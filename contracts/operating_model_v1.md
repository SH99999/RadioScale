# RadioScale Operating Model v1

This is the single operating-model truth for this repository.

## Branch model
- `main` is the only truth.
- Product development runs on `dev/*` (optional `dev/ux`).
- `si/governance` is the single governance lane (exceptional, not product development).
- `ops/chat-archive` is archive/input only, never truth, never merged into `main`.
- `work` and `temp_*` are invalid branches.

## Delivery model
- Codex develops on `dev/*`, tests, and prepares PRs to `main`.
- One package may touch multiple components.
- Owner can hand over directly in Codex chat.
- Optional file handoff exists on `ops/chat-archive`.
- Archive intake is auto-routed by `archive-handoff-auto-route-v1` on a 5-minute scheduler from `main`; no manual workflow click is required.
- Owner does not manually move handoff files between branches.
- Codex bridges archive intake into implementation flow.
- Intake automation auto-creates routing issues and ensures a draft PR exists for each target `dev/*` branch.

## Status + context model
- Keep `status/*.yaml` and `context/*.md` short and factual.
- Allowed status values are only component-delivery statuses: `backlog`, `open`, `in_progress`, `on_hold`, `done` (no extra chat lifecycle statuses in RadioScale truth).

## Merge-clean and drift ownership
- Codex owns keeping branches refreshed/rebased; `dev-branch-refresh-v1` keeps branch drift down automatically.
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
