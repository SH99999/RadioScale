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
