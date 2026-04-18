# Deployment Contract v1

Operating model reference: `contracts/operating_model_v1.md`.

## Standard
- Deploy/rollback to Pi is Git-driven and repo-controlled.
- Manual Pi shell install/fix is not normal delivery.

## Required automation
- `.github/workflows/component-test-deploy-v10.yml`
- `.github/workflows/component-test-rollback-v10.yml`
- `.github/workflows/component-test-release-slot-v3.yml`
- `tools/deploy/pi-bootstrap-v1.sh` must run before deploy/rollback.

## Requirements
- bootstrap/deploy scripts are idempotent
- rollback path is repo-controlled
- dependency/setup drift on Pi is a blocker to eliminate in repo scripts

## PR evidence minimum
- deploy evidence
- rollback evidence (`not-applicable` allowed)
- exact `git_ref`, `component`, `payload`, `target`
