# RadioScale Autodeploy and Rollout v1

## Purpose
Provide the minimum operational runbook for rollout/deploy/rollback with GitHub Actions.

## Active workflows
- `.github/workflows/component-test-deploy-v10.yml`
- `.github/workflows/component-test-rollback-v10.yml`
- `.github/workflows/component-test-release-slot-v3.yml`
- `.github/workflows/ci-shell-syntax-v1.yml`

## Supported components for deploy wrapper
- `tuner`
- `fun-line`
- `bridge`

## Deterministic rollout path
1. Push changes on a non-`main` branch.
2. Open PR and run CI shell syntax checks.
3. Run `component-test-deploy-v10` against test target.
4. Run runtime validation on target and collect evidence.
5. If needed run `component-test-rollback-v10`.
6. Release target slot with `component-test-release-slot-v3`.
7. Merge to `main` after owner acceptance.

## Required runtime evidence
- deploy workflow run URL
- rollback workflow run URL (or `not-applicable`)
- target slot state result (`test_open`, `released`, or `blocked`)
- exact branch/ref and payload used
