# Autodeploy and Rollout v1

Operating model reference: `contracts/operating_model_v1.md`.

## Standard rule
Deploy and rollback to Pi are Git-driven and repo-controlled.
Manual Pi shell install/fix is not normal delivery.

## Active workflows
- `.github/workflows/component-test-deploy-v10.yml`
- `.github/workflows/component-test-rollback-v10.yml`
- `.github/workflows/component-test-release-slot-v3.yml`

## Repo-controlled bootstrap
- Workflows run `tools/deploy/pi-bootstrap-v1.sh` before deploy/rollback.
- Bootstrap must install required runtime dependencies and setup idempotently.
- Bootstrap failure is a blocker to fix in repo scripts/workflows.

## Required deploy evidence
- deploy run URL
- rollback run URL or `not-applicable`
- exact `git_ref`, `component`, `payload`, `target`
