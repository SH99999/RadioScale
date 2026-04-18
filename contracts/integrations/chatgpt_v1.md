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
- scheduled workflow `.github/workflows/archive-handoff-auto-route-v1.yml` pulls `ops/chat-archive` handoff files and auto-creates routing issues
