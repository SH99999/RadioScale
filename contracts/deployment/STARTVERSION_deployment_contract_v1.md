# STARTVERSION Deployment Contract v1

## Objective
Ship safely with minimal ceremony.

## 1) Pre-deploy requirements
- Build/runtime checks pass for changed component(s).
- Deploy target and release identifier are explicit.
- Rollback target is explicit.

## 2) Deployment execution
- One active deployment target slot at a time per target environment.
- Run deploy steps deterministically from repo-truth artifacts.
- Record deployed version and timestamp.

## 3) Rollback requirements
- Every deployable release must have one tested rollback path.
- Rollback command must be included in PR packet.

## 4) Promotion gate to `main`
A release is merge-ready only when:
- checks passed,
- deploy/rollback evidence recorded,
- owner decision captured.

## 5) Git automation baseline (required)
- `ci-shell-syntax-v1` must run on push/PR for script syntax guardrails.
- `component-test-deploy-v10` is the canonical deploy test entrypoint.
- `component-test-rollback-v10` is the canonical rollback entrypoint.
- `component-test-release-slot-v3` is the canonical slot release entrypoint.
- Deploy/rollback workflows are run as `workflow_dispatch` with explicit `component`, `git_ref`, `payload`, and `target`.
