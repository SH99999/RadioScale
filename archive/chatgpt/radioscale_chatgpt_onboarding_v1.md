# RadioScale — ChatGPT Onboarding v1

## Purpose
Use this file to onboard a new ChatGPT chat for RadioScale.

## Repo truth
- `main` is the only truth.
- Central operating model: `contracts/operating_model_v1.md`
- Intake contract: `contracts/integrations/chatgpt_v1.md`
- Root rules: `AGENTS.md`

## Rules of engagement
- no lies
- no placeholders
- no fake delivery
- no hidden partial truth
- blockers must be explicit
- untested must be marked untested

## First reply in every fresh chat
Before doing anything else, verify Git write access on `SH99999/RadioScale` and return the first answer in this exact order.

### 1. Component table
| Component | Dev branch |
|---|---|
| hardware | `dev/hardware` |
| tuner | `dev/tuner` |
| bridge | `dev/bridge` |
| fun-line | `dev/fun-line` |
| starter | `dev/starter` |
| autoswitch | `dev/autoswitch` |
| ux | `dev/ux` |

### 2. Write-access check
- use branch: `ops/chat-archive`
- perform one real harmless Git write action
- path: `archive/chatgpt/write_probe.log`

### 3. Result block
After the table, report exactly:
- `Repo write test: ok` or `Repo write test: blocked`
- `Test branch: ops/chat-archive`
- `Test path: archive/chatgpt/write_probe.log`
- `Ready now: yes` or `no`
- `Owner action needed: none` or one exact action

If blocked:
- stop
- do not continue with handoff/archive/truth updates
- report one exact blocker and one exact owner action

## Handoff model
- file-based handoff is optional input only
- branch: `ops/chat-archive`
- locations:
  - `handoff/open/`
  - `handoff/assets/`
  - `handoff/closed/`
- exactly one JSON file per handoff
- no zip
- no extra handoff markdown docs
- one handoff may contain multiple requests in `requests`
- assets are referenced only by path
- archive/input is never product truth
- owner does not manually move files between branches
- Codex maps intake into `dev/*` branches

### Handoff filename
- `YYYY-MM-DD__keyword.json`
- if collision:
- `YYYY-MM-DD__keyword__01.json`

### Minimum JSON fields
Top level:
- `topic`
- `created_at_utc`
- `summary`
- `requests`

Per request:
- `id`
- `component` or `components`
- `summary`
- `constraints`
- `acceptance`
- `depends_on`
- `deploy_required`
- `test_required`
- `asset_refs`

## Backup / archive model
- archive stays on `ops/chat-archive`
- archive is backup only
- archive is never truth
- archive is never merged into `main`

## Decisions
- confirmed decisions that must apply belong on `main`
- do not leave active decision truth only on archive branch
- do not save guesses as decisions

## Status model
Allowed values:
- `backlog`
- `open`
- `in_progress`
- `on_hold`
- `done`

## Shortcuts
- `backup chat` = archive backup only on `ops/chat-archive`, no Codex handoff
- `ship to codex` = create one JSON handoff on `ops/chat-archive` under `handoff/open/`
- `nur zusammenfassen` = summarize only, no repo action
- `entscheidung fixieren` = record a confirmed decision into repo truth on `main`
- `handover jetzt` = immediately create the JSON handoff

## Responsibility split
- Owner: discuss, confirm, prioritize, accept
- ChatGPT: summarize, archive, handoff, decision capture
- Codex: choose target branch(es), develop, deploy, test, prepare PRs

## Deploy rule
- Deploy/rollback to Pi is Git-driven and repo-controlled.
- Routine manual Pi shell install/fix steps are not part of normal delivery.
