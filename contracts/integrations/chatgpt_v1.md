# ChatGPT/Codex Intake Contract v1 (RadioScale)

## Purpose
Define minimal intake into Codex execution.

## Source of truth
Operating doctrine and statuses are defined only in `contracts/repo/STARTVERSION_repo_operating_contract_v1.md`.
This file defines intake interface only.

## Intake sources
- owner direct in Codex chat
- one JSON handoff file on archive branch `ops/chat-archive` under `handoff/open/`

## Intake payload rule
- One handoff JSON may contain multiple requests.
- Codex decides target component branch mapping and implementation split.
- Codex runs `tools/intake/consume_archive_handoff_v1.py` to bridge archive input into active development flow.

## Request minimum fields
- `id`
- `component` or `components`
- `summary`
- `constraints`
- `acceptance`
- `depends_on`
- `deploy_required`
- `test_required`
- `asset_refs`

## Constraints
- Archive branch data is input/archive only and never product truth.
- Owner must not manually shuttle handoff files between branches.
- no fake delivery
- no hidden partial truth
- blockers must be explicit
