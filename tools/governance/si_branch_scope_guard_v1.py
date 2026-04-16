#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path
import re

GOVERNED_PATH_PATTERNS = [
    re.compile(r"^contracts/repo/"),
    re.compile(r"^docs/agents/"),
    re.compile(r"^journals/system-integration-normalization/"),
    re.compile(r"^tools/governance/"),
    re.compile(r"^\.github/workflows/"),
]


def is_governed(path: str) -> bool:
    return any(rx.search(path) for rx in GOVERNED_PATH_PATTERNS)


def main() -> int:
    parser = argparse.ArgumentParser(description="Guard SI/governance file mutations to si/* branches.")
    parser.add_argument("--branch", required=True, help="Current branch name (typically PR head branch)")
    parser.add_argument("--changed-files", required=True, help="Path to file containing changed paths, one per line")
    parser.add_argument("--enforce", default="true", choices=["true", "false"], help="Fail when rule is violated")
    args = parser.parse_args()

    changed_file_path = Path(args.changed_files)
    if not changed_file_path.exists():
        print(f"si_branch_scope_guard=fail\nmissing_changed_files_input:{changed_file_path}")
        return 1

    changed_files = [line.strip() for line in changed_file_path.read_text(encoding="utf-8").splitlines() if line.strip()]
    governed_changes = [path for path in changed_files if is_governed(path)]

    if not governed_changes:
        print("si_branch_scope_guard=ok")
        print("governed_changes=0")
        return 0

    branch_ok = args.branch.startswith("si/")
    if branch_ok:
        print("si_branch_scope_guard=ok")
        print(f"governed_changes={len(governed_changes)}")
        return 0

    print("si_branch_scope_guard=violation")
    print(f"branch={args.branch}")
    print(f"governed_changes={len(governed_changes)}")
    for path in governed_changes:
        print(f"changed_governed_path:{path}")

    if args.enforce == "true":
        print("result=fail (SI_BRANCH_GUARD_ENFORCE=true)")
        return 1

    print("result=warn-only (SI_BRANCH_GUARD_ENFORCE=false)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
