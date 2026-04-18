# ChatGPT/Codex Intake Contract v1 (RadioScale)

## Purpose
Define lightweight intake from owner/ChatGPT into Codex execution.

## Source of truth
- Operating doctrine and statuses are defined only in `contracts/repo/STARTVERSION_repo_operating_contract_v1.md`.
- This file defines intake interface only.

## Intake sources
- owner direct in Codex chat
- one JSON handover file in `handoff/open/`

## Intake payload rule
- One handover JSON may contain multiple requests.
- Codex decides target component branch mapping.

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
- no fake delivery
- no hidden partial truth
- blockers must be explicit
