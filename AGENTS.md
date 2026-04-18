# AGENTS.md (RadioScale)

## Scope
This file applies to the whole repository.

## Operating rules (mandatory)
1. Work from Git branches only (`main`, `dev/*`, `si/*`, `temp_codex`).
2. Never use local-only branch `work`.
3. Push branch changes to `origin` before reporting completion.
4. `main` is protected truth; changes land through PR.
5. Keep repository docs minimal and aligned to the RadioScale operating model.
6. Remove stale/legacy markdown surfaces when they are not execution-relevant.
7. If blocked, report exact blocker and required owner decision in one line.

## Branch intent
- `main`: accepted stable truth
- `dev/*`: active component implementation
- `si/*`: orchestration and cross-component control-plane updates
- `temp_codex`: temporary integration lane for consolidation work
