# ChatGPT/Codex Intake Contract v1 (RadioScale)

## Purpose
Define minimal, deterministic intake/routing for owner + ChatGPT + Codex.

## Truth order
1. repo contracts
2. branch commits and PR state
3. issue state/comments

## Intake sources
- owner direct in Codex chat
- JSON handover in `handoff/open/`

## Routing model
- Codex maps each request to target branch/component.
- One intake may contain multiple component requests.
- Statuses: `backlog`, `open`, `in_progress`, `on_hold`, `done`.

## Done evidence (required)
- `test_evidence`
- `rollback_evidence`

## Constraints
- no fake delivery
- no hidden partial truth
- blockers must be explicit
