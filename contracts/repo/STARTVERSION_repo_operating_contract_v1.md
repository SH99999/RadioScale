# STARTVERSION Repo Operating Contract v1

## Single operating-model truth
This file is the canonical operating model for RadioScale.
Other docs may link to this file but must not redefine branch doctrine, status doctrine, handoff doctrine, or merge-clean rules.

## Truth and branches
- `main` is the only accepted truth.
- No direct commits to `main`; PR required.
- Product development branches: `dev/*`.
- Optional UX lane: `dev/ux`.
- Governance-only lane: `si/*` (contracts/process docs only, not product implementation).
- `temp_*` and `work` branches are invalid operating lanes.

## Git-only execution
- Every agent works on a Git-tracked branch and pushes before reporting done.
- Local-only completion claims are invalid.

## Lean delivery model
- One package may include multiple components.
- Codex determines technical split per component branch.
- Keep docs minimal; delete stale/duplicate operating text.

## Status model
Allowed statuses: `backlog`, `open`, `in_progress`, `on_hold`, `done`.

## Done evidence (required)
- `test_evidence`
- `rollback_evidence`

## Archive/input branch model (handoff + backups)
- Handoff JSON and raw ChatGPT/Codex backups live only on `ops/chat-archive`.
- `ops/chat-archive` is archive/input only, never truth.
- `ops/chat-archive` is never merged into `main`.
- Owner does not move files between branches.
- Codex reads intake from `ops/chat-archive` and routes implementation into `dev/*`.

## Branch drift and merge-clean ownership
- Codex owns branch refresh/rebase for active development branches.
- Codex owns PR merge-clean readiness before owner review.
- Owner should not resolve routine merge conflicts.
- Repo guard: PRs to `main` must pass merge-clean check (`pr-merge-clean-v1`).

## Deploy-to-Pi operating rule (mandatory)
- Standard path is Git-driven deploy/rollback via repo workflows and scripts.
- Routine deployment must not require manual Pi shell install/fix steps.
- Runtime dependencies, setup actions, permissions, and service actions must be handled by repo-controlled bootstrap/deploy scripts.
- Deploy scripts must be idempotent.
- Rollback must remain repo-controlled.
- Any remaining manual Pi prerequisite is a blocker to eliminate, not an accepted normal step.

## Non-negotiables
- no fake delivery
- no hidden partial truth
- blockers explicit and actionable
