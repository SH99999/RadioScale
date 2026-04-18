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
- Commits on supported delivery branches (`dev/tuner`, `dev/bridge`, `dev/fun-line`) trigger repo-controlled Pi autodeploy from that branch (`dev-autodeploy-on-push-v1`).
- One package may touch multiple components.
- Owner can hand over directly in Codex chat.
- Optional file handoff exists on `ops/chat-archive`.

## Regular intake-to-execution process (mandatory)
1. `archive-handoff-auto-route-v1` triggers on push to `ops/chat-archive/handoff/open/*.json` (plus 1-minute scheduler fallback) and reads archive handoff JSONs.
2. Intake is validated and mapped to target `dev/*` branches.
3. Routing issues are created/updated automatically.
4. `issue-autostart-v1` immediately moves handoff issues to `status/in_progress`, links target branch, and starts execution kickoff on the target `dev/*` branch.
5. The same listener writes kickoff commit evidence, ensures a draft PR exists for the target branch, and writes commit/PR links back to the issue.
6. Codex continues implementation commits on the same branch until review-ready.

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
