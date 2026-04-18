# RadioScale Autodeploy and Rollout v1

## Active workflows
- `.github/workflows/ci-shell-syntax-v1.yml`
- `.github/workflows/component-test-deploy-v10.yml`
- `.github/workflows/component-test-rollback-v10.yml`
- `.github/workflows/component-test-release-slot-v3.yml`

## Deploy support matrix
- `tuner`
- `fun-line`
- `bridge`

## Execution path
1. Implement on branch (`dev/*` or `si/*`).
2. Open PR and pass CI shell syntax check.
3. Run deploy workflow (target + component + git_ref + payload).
4. Validate runtime.
5. Run rollback workflow when required.
6. Release slot.
7. Merge after owner acceptance.

## Required evidence
- deploy run URL
- rollback run URL or `not-applicable`
- exact `git_ref`, `component`, `payload`, `target`
