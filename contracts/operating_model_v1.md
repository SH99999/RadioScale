# RadioScale Operating Model v1

This is the single operating-model truth for this repository.

## Branch model
- `main` is the only truth.
- Product development runs on `dev/*` (optional `dev/ux`).
- `si/*` is governance-only and exceptional.
- `ops/chat-archive` is archive/input only, never truth, never merged into `main`.
- `work` and `temp_*` are invalid branches.

## Delivery model
- Codex develops on `dev/*`, tests, and prepares PRs to `main`.
- One package may touch multiple components.
- Owner can hand over directly in Codex chat.
- Optional file handoff exists on `ops/chat-archive`.
- Archive intake is auto-routed from `ops/chat-archive` by scheduled workflow (`archive-handoff-auto-route-v1`); no manual workflow click is required.
- Owner does not manually move handoff files between branches.
- Codex bridges archive intake into implementation flow.

## Status + context model
- Keep `status/*.yaml` and `context/*.md` short and factual.
- Allowed status values: `backlog`, `open`, `in_progress`, `on_hold`, `done`.

## Merge-clean and drift ownership
- Codex owns keeping branches refreshed/rebased.
- Codex owns keeping PRs merge-clean before review.
- Owner should not resolve routine merge conflicts.

## Deploy model (mandatory)
- Deploy/rollback to Pi is Git-driven and repo-controlled.
- Routine manual Pi shell install/fix steps are not part of normal delivery.
- Bootstrap/deploy scripts must be idempotent.
- Remaining manual dependency steps are blockers to eliminate.

## Non-negotiables
- no fake delivery
- no hidden partial truth
- blockers explicit and actionable
