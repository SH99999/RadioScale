# ChatGPT Integration Contract v1 (RadioScale)

## Purpose
Define a minimal, deterministic rule set for using GitHub Issues with ChatGPT/Codex intake and delivery.

## Direct answer
- GitHub Issues help the process when used as a routing/dispatch surface.
- GitHub Issues are **not** the canonical execution truth by themselves.
- Canonical truth remains: repo artifacts + branch commits + PR state.

## Canonical truth order
1. contracts in repository
2. ChatGPT demand/protocol artifacts in repository (when present)
3. branch/commit/PR evidence
4. issue status and discussion

## Issue usage rule
- Use issues for intake triage, work splitting, and dispatch visibility.
- Do not treat issue comments as completion proof.
- Completion proof must be commit + checks + PR + merge/closeout evidence.

## Codex execution authority
Codex may do either path from one intake:
1. **self-implement path**  
   - create/update issue  
   - create branch  
   - implement + run checks  
   - push + open/update PR  
   - update issue with PR and result
2. **dispatch path**  
   - create/update issue  
   - split into scoped child issues if needed  
   - assign dispatch target (agent/lane)  
   - verify delivered PRs  
   - close issue only after merge or explicit owner rejection

## Required issue fields (minimum)
- `intake_source` (chat, zip, demand path, or protocol path)
- `execution_mode` (`self-implement` | `dispatch`)
- `target_branch` (or branch pattern)
- `done_definition`
- `rollback_command` (or `not-applicable`)

## Operational guardrails
- One issue may map to multiple PRs; each PR must be linked back in the issue.
- If intake is ambiguous, Codex must write one clarification comment and proceed with the safest bounded scope.
- If high-risk or governance-conflict changes are detected, escalate to owner decision before merge.

## Outcome requirement
Every closed issue must have:
- linked merged PR(s) or explicit owner rejection reference
- final status (`delivered` | `rejected` | `blocked`)
- evidence links for checks/run results
