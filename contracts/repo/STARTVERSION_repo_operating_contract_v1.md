# STARTVERSION Repo Operating Contract v1

## Truth and branches
- `main` is the only accepted truth.
- No direct commits to `main`; PR required.
- Working branches: `dev/*`, `si/*`, `temp_codex`.
- Branch `work` is forbidden.

## Git-only execution
- Every agent must work on a Git-tracked branch and push before reporting done.
- Local-only completion claims are invalid.

## Delivery model
- One package may cover multiple components.
- Codex owns technical split and routing.
- Keep docs and artifacts minimal; remove stale markdown/process noise.

## Status model
Allowed statuses: `backlog`, `open`, `in_progress`, `on_hold`, `done`.

## Done evidence
- `test_evidence`
- `rollback_evidence`

## Non-negotiables
- no fake delivery
- no hidden partial truth
- blockers explicit and actionable
