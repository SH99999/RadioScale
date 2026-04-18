# STARTVERSION Repo Operating Contract v1

## Single operating-model truth
This file is the canonical operating model for RadioScale.
Other docs may link to this file but must not redefine branch doctrine, status doctrine, or handover doctrine.

## Truth and branches
- `main` is the only accepted truth.
- No direct commits to `main`; PR required.
- Product development branches: `dev/*`.
- Optional UX lane: `dev/ux`.
- Governance-only lane: `si/*` (governance contracts/process docs only, not normal product implementation).
- Branch `work` and temporary integration lanes are invalid.

## Git-only execution
- Every agent works on a Git-tracked branch and pushes before reporting done.
- Local-only completion claims are invalid.

## Lean delivery model
- One package may include multiple components.
- Codex determines technical split per component branch.
- Handover is lightweight input; repo state + PR evidence is truth.
- Keep docs minimal; delete stale/duplicate operating text.

## Status model
Allowed statuses: `backlog`, `open`, `in_progress`, `on_hold`, `done`.

## Done evidence (required)
- `test_evidence`
- `rollback_evidence`

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
