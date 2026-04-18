# STARTVERSION Deployment Contract v1

## Objective
Ship safely with minimal ceremony through repo-controlled automation.

## Mandatory deployment surface
- Standard delivery is GitHub workflow + repo deploy scripts.
- Manual Pi shell install/fix steps are not accepted as normal workflow.

## 1) Pre-deploy requirements
- Checks pass for changed component(s).
- Deploy target and release identifier are explicit.
- Rollback target is explicit.

## 2) Deployment execution
- One active deployment target slot at a time per target environment.
- Pi bootstrap runs from repo script before deploy/rollback.
- Deploy steps run deterministically from repository artifacts.
- Re-running bootstrap/deploy must be idempotent.
- Record deployed version and timestamp.

## 3) Rollback requirements
- Every deployable release has one repo-controlled rollback path.
- Rollback command must be included in PR packet.

## 4) Promotion gate to `main`
A release is merge-ready only when:
- checks passed,
- deploy/rollback evidence recorded,
- owner decision captured.

## 5) Git automation baseline (required)
- `ci-shell-syntax-v1` is required on push/PR.
- `component-test-deploy-v10` is the canonical deploy entrypoint.
- `component-test-rollback-v10` is the canonical rollback entrypoint.
- `component-test-release-slot-v3` is the canonical slot release entrypoint.
- Deploy/rollback workflows run as `workflow_dispatch` with explicit `component`, `git_ref`, `payload`, and `target`.
- Workflows must run `tools/deploy/pi-bootstrap-v1.sh` so dependencies/setup stay repo-controlled.

## 6) Manual dependency drift policy
If deployment still requires manual dependency installation on Pi, treat that as a blocker and absorb it into repo bootstrap scripts/workflows.
