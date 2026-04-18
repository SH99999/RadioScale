#!/usr/bin/env python3
"""Bridge archive handoff intake into active development routing.

Reads JSON handoff files from origin/ops/chat-archive:handoff/open/, validates
minimum fields, and prints deterministic routing hints for dev/* branches.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
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


@dataclass
class IntakeResult:
    file_path: str
    request_id: str
    component: str
    branch: str


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


def to_branch(component: str) -> str:
    normalized = component.strip().lower().replace("_", "-")
    if normalized == "ux":
        return "dev/ux"
    return f"dev/{normalized}"


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
            routed.append(
                IntakeResult(
                    file_path=path,
                    request_id=request_id,
                    component=comp,
                    branch=to_branch(comp),
                )
            )
    return routed


def main() -> int:
    parser = argparse.ArgumentParser(description="Consume archive handoff JSON from ops/chat-archive")
    parser.add_argument("--branch", default=ARCHIVE_BRANCH_DEFAULT, help="Archive branch ref")
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
    for file_path in files:
        try:
            routed = parse_handoff(file_path, get_file_text(args.branch, file_path))
            for entry in routed:
                print(f"{entry.file_path} | request={entry.request_id} | component={entry.component} | target_branch={entry.branch}")
        except Exception as exc:  # noqa: BLE001
            failures += 1
            print(f"{file_path} | ERROR: {exc}")

    if failures:
        print(f"Completed with {failures} invalid handoff file(s).")
        return 1

    print("Completed with all handoff files validated and routed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
