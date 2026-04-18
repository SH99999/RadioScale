# ChatGPT/Codex Intake Contract v1

Purpose: define lightweight intake only.

Operating rules live only in `contracts/operating_model_v1.md`.

## Intake sources
- owner direct in Codex chat
- optional JSON handoff on `ops/chat-archive` under `handoff/open/`

## Minimum request fields
- `id`
- `component` or `components`
- `summary`
- `constraints`
- `acceptance`
- `depends_on`
- `deploy_required`
- `test_required`
- `asset_refs`

## Required behavior
- archive branch content is input/archive only, never product truth
- owner does not shuttle files between branches
- Codex maps intake into `dev/*` implementation branches
- `archive-handoff-auto-route-v1` runs on `push` to `ops/chat-archive/handoff/open/*.json` and also every minute from `main`; it reads archive handoff JSONs and creates/updates routing issues
- `issue-autostart-v1` runs on those issues, sets `status/in_progress`, starts kickoff commit on target `dev/*`, ensures draft PR, and links commit/PR back to issue
- this listener chain is part of the regular process, not an exception path

## Lean status boundary
- `ready-for-codex` is not part of RadioScale operating truth.
- RadioScale uses only the minimal component-delivery status set defined in `contracts/operating_model_v1.md`.
