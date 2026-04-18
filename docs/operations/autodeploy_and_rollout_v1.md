# RadioScale Autodeploy and Rollout v1

## Standard operating rule
Deploy and rollback to the Pi are Git-driven and repo-controlled.
Manual Pi shell install/fix steps are not part of normal delivery.

## Active workflows
- `.github/workflows/ci-shell-syntax-v1.yml`
- `.github/workflows/component-test-deploy-v10.yml`
- `.github/workflows/component-test-rollback-v10.yml`
- `.github/workflows/component-test-release-slot-v3.yml`

## Supported components
- `tuner`
- `fun-line`
- `bridge`

## Execution path
1. Implement on component branch (`dev/*`).
2. Open PR and pass CI shell syntax check.
3. Run deploy workflow with explicit `target`, `component`, `git_ref`, and `payload`.
4. Validate runtime.
5. Run rollback workflow when required.
6. Release target slot.
7. Merge after owner acceptance.

## Repo-controlled Pi bootstrap
- Workflow bootstrap step runs `tools/deploy/pi-bootstrap-v1.sh` before deploy/rollback.
- Bootstrap installs missing runtime dependencies and creates required directories idempotently.
- Any bootstrap failure is a blocker and must be fixed in repo scripts/workflows.

## Required evidence
- deploy run URL
- rollback run URL or `not-applicable`
- exact `git_ref`, `component`, `payload`, `target`
