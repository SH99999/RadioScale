#!/usr/bin/env python3
"""Bridge archive handoff intake into active development routing.

Reads JSON handoff files from origin/ops/chat-archive:handoff/open/, validates
minimum fields, normalizes component aliases, and emits deterministic routing
entries for dev/* branches.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from typing import Iterable

ARCHIVE_BRANCH_DEFAULT = "origin/ops/chat-archive"
OPEN_PREFIX = "handoff/open/"
REQUIRED_FIELDS = {
    "id",
    "summary",
    "constraints",
    "acceptance",
    "depends_on",
    "deploy_required",
    "test_required",
    "asset_refs",
}
COMPONENT_ALIASES = {
    "scale": "bridge",
    "radio-scale": "bridge",
    "radio_scale": "bridge",
}
KNOWN_COMPONENTS = {
    "tuner",
    "bridge",
    "fun-line",
    "starter",
    "autoswitch",
    "hardware",
    "ux",
}


@dataclass
class IntakeResult:
    file_path: str
    request_id: str
    component: str
    branch: str
    summary: str
    acceptance: str
    constraints: str


def run_git(*args: str) -> str:
    proc = subprocess.run(["git", *args], check=False, capture_output=True, text=True)
    if proc.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)} failed: {proc.stderr.strip()}")
    return proc.stdout


def list_archive_json(branch: str) -> list[str]:
    output = run_git("ls-tree", "-r", "--name-only", branch, OPEN_PREFIX)
    return sorted([line.strip() for line in output.splitlines() if line.strip().endswith(".json")])


def get_file_text(branch: str, path: str) -> str:
    return run_git("show", f"{branch}:{path}")


def normalize_components(request: dict) -> Iterable[str]:
    if "component" in request and request["component"]:
        yield str(request["component"])
    for comp in request.get("components", []) or []:
        yield str(comp)


def canonical_component(component: str) -> str:
    normalized = component.strip().lower().replace("_", "-")
    return COMPONENT_ALIASES.get(normalized, normalized)


def to_branch(component: str) -> str:
    canon = canonical_component(component)
    if canon not in KNOWN_COMPONENTS:
        raise ValueError(
            f"unknown component '{component}' (canonical '{canon}'). "
            f"Known: {', '.join(sorted(KNOWN_COMPONENTS))}"
        )
    return "dev/ux" if canon == "ux" else f"dev/{canon}"


def validate_request(request: dict) -> None:
    missing = sorted(REQUIRED_FIELDS.difference(request.keys()))
    if missing:
        raise ValueError(f"missing required fields: {', '.join(missing)}")
    if not (request.get("component") or request.get("components")):
        raise ValueError("missing component/components")


def parse_handoff(path: str, text: str) -> list[IntakeResult]:
    payload = json.loads(text)
    requests = payload.get("requests", [])
    if not isinstance(requests, list) or not requests:
        raise ValueError("handoff must contain non-empty requests[]")

    routed: list[IntakeResult] = []
    for req in requests:
        validate_request(req)
        request_id = str(req["id"])
        for comp in normalize_components(req):
            canon = canonical_component(comp)
            routed.append(
                IntakeResult(
                    file_path=path,
                    request_id=request_id,
                    component=canon,
                    branch=to_branch(comp),
                    summary=str(req.get("summary", "")).strip(),
                    acceptance=str(req.get("acceptance", "")).strip(),
                    constraints=str(req.get("constraints", "")).strip(),
                )
            )
    return routed


def github_api_request(url: str, token: str, payload: dict | None = None, method: str = "GET") -> dict | list:
    data = None
    if payload is not None:
        data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data,
        method=method,
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
            "Content-Type": "application/json",
        },
    )
    with urllib.request.urlopen(req) as resp:  # noqa: S310
        raw = resp.read().decode("utf-8")
        if not raw:
            return {}
        return json.loads(raw)


def ensure_issue(entry: IntakeResult, repo: str, token: str) -> str:
    title = f"[handoff] {entry.request_id} -> {entry.branch}"
    q = urllib.parse.quote(f'repo:{repo} is:issue is:open in:title "{title}"')
    search_url = f"https://api.github.com/search/issues?q={q}"
    found = github_api_request(search_url, token)
    items = found.get("items", []) if isinstance(found, dict) else []
    if items:
        return items[0].get("html_url", "")

    body = (
        f"source_handoff: `{entry.file_path}`\n"
        f"request_id: `{entry.request_id}`\n"
        f"target_branch: `{entry.branch}`\n"
        f"component: `{entry.component}`\n\n"
        f"summary:\n{entry.summary or '-'}\n\n"
        f"acceptance:\n{entry.acceptance or '-'}\n\n"
        f"constraints:\n{entry.constraints or '-'}\n"
    )
    created = github_api_request(
        f"https://api.github.com/repos/{repo}/issues",
        token,
        payload={"title": title, "body": body},
        method="POST",
    )
    if isinstance(created, dict):
        return created.get("html_url", "")
    return ""


def ensure_pr(branch: str, repo: str, token: str) -> str:
    owner = repo.split("/")[0]
    pulls = github_api_request(
        f"https://api.github.com/repos/{repo}/pulls?state=open&head={owner}:{branch}",
        token,
    )
    if isinstance(pulls, list) and pulls:
        return pulls[0].get("html_url", "")

    created = github_api_request(
        f"https://api.github.com/repos/{repo}/pulls",
        token,
        payload={
            "title": f"[autostart] {branch} intake execution",
            "head": branch,
            "base": "main",
            "body": (
                "Auto-opened by archive handoff routing automation.\n\n"
                f"- target_branch: `{branch}`\n"
                "- purpose: immediate development lane visibility (no owner manual start click)\n"
                "- note: implementation commits are produced by Codex on this branch\n"
            ),
            "draft": True,
        },
        method="POST",
    )
    if isinstance(created, dict):
        return created.get("html_url", "")
    return ""


def main() -> int:
    parser = argparse.ArgumentParser(description="Consume archive handoff JSON from ops/chat-archive")
    parser.add_argument("--branch", default=ARCHIVE_BRANCH_DEFAULT, help="Archive branch ref")
    parser.add_argument("--json-output", default="", help="Optional path to write routing json")
    parser.add_argument("--auto-issue", action="store_true", help="Create/open issues automatically")
    parser.add_argument("--auto-pr", action="store_true", help="Ensure draft PR exists for each target dev branch")
    parser.add_argument("--repo", default=os.getenv("GITHUB_REPOSITORY", ""), help="GitHub repo owner/name")
    args = parser.parse_args()

    try:
        run_git("fetch", "origin", "ops/chat-archive", "--quiet")
        files = list_archive_json(args.branch)
    except RuntimeError as exc:
        print(f"ERROR: {exc}")
        return 2

    if not files:
        print("No archive handoff JSON files found under handoff/open/.")
        return 0

    print("Archive intake routing plan")
    print("===========================")

    failures = 0
    all_entries: list[IntakeResult] = []
    for file_path in files:
        try:
            routed = parse_handoff(file_path, get_file_text(args.branch, file_path))
            all_entries.extend(routed)
            for entry in routed:
                print(
                    f"{entry.file_path} | request={entry.request_id} | component={entry.component} | "
                    f"target_branch={entry.branch}"
                )
        except Exception as exc:  # noqa: BLE001
            failures += 1
            print(f"{file_path} | ERROR: {exc}")

    issue_urls: list[str] = []
    pr_urls: list[str] = []
    if (args.auto_issue or args.auto_pr) and failures == 0:
        token = os.getenv("GITHUB_TOKEN") or os.getenv("GH_TOKEN")
        if not token:
            print("ERROR: --auto-issue/--auto-pr requires GITHUB_TOKEN/GH_TOKEN")
            return 2
        if not args.repo:
            print("ERROR: --auto-issue/--auto-pr requires --repo or GITHUB_REPOSITORY")
            return 2

        if args.auto_issue:
            for entry in all_entries:
                try:
                    url = ensure_issue(entry, args.repo, token)
                    if url:
                        issue_urls.append(url)
                        print(f"issue: {url}")
                except urllib.error.HTTPError as exc:
                    failures += 1
                    print(f"issue ERROR ({entry.request_id}/{entry.component}): {exc}")

        if args.auto_pr:
            for branch in sorted({entry.branch for entry in all_entries}):
                try:
                    url = ensure_pr(branch, args.repo, token)
                    if url:
                        pr_urls.append(url)
                        print(f"pr: {url}")
                except urllib.error.HTTPError as exc:
                    body = exc.read().decode("utf-8", errors="replace")
                    if exc.code == 422 and ("No commits between" in body or "A pull request already exists" in body or "no history in common" in body.lower()):
                        print(f"pr SKIP ({branch}): {exc.code} {body.strip()}")
                        continue
                    failures += 1
                    print(f"pr ERROR ({branch}): {exc} {body.strip()}")

    if args.json_output:
        payload = {
            "entries": [
                {
                    "file_path": e.file_path,
                    "request_id": e.request_id,
                    "component": e.component,
                    "branch": e.branch,
                }
                for e in all_entries
            ],
            "issue_urls": issue_urls,
            "pr_urls": pr_urls,
            "failures": failures,
        }
        with open(args.json_output, "w", encoding="utf-8") as fh:
            json.dump(payload, fh, indent=2)

    if failures:
        print(f"Completed with {failures} failure(s).")
        return 1

    print("Completed with all handoff files validated and routed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
