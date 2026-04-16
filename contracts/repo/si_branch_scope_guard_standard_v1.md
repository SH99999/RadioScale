# SI BRANCH SCOPE GUARD STANDARD V1

## Purpose
Prevent SI/governance truth mutations from being delivered on non-`si/*` branches.

## Guard scope
The guard applies to pull requests that mutate governed files under:
- `contracts/repo/`
- `docs/agents/`
- `journals/system-integration-normalization/`
- `tools/governance/`
- `.github/workflows/`

## Rule
- if governed files are changed, PR head branch must match `si/<topic>`
- if no governed files are changed, guard returns `ok`

## Implementation
- Script: `tools/governance/si_branch_scope_guard_v1.py`
- Workflow: `.github/workflows/si-branch-scope-guard-v1.yml`

## Rollback
- temporary warn-only mode: set repository variable `SI_BRANCH_GUARD_ENFORCE=false`
- hard rollback: revert workflow/script commit

## Safety
On violation, the guard must print changed governed paths and branch name to keep owner triage explicit.
