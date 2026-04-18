# AGENTS.md (RadioScale)

## Scope
This file applies to the whole repository.

## Central operating truth
- Canonical operating model: `contracts/repo/STARTVERSION_repo_operating_contract_v1.md`.
- Do not restate or fork operating doctrine in local docs.

## Mandatory execution rules
1. Use Git branches only (`main`, `dev/*`, `si/*`).
2. `si/*` is governance-only (contracts/process/docs). Product development runs on `dev/*`.
3. Never use local-only branch `work`.
4. Push branch changes to `origin` before reporting completion.
5. `main` is protected truth; land changes through PR.
6. If blocked, report one explicit blocker and the one owner decision needed.
