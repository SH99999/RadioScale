# Deploy Contract V2 — Tuner First

This document explains the practical rollout choice:
- Deploy V2 is introduced for the Tuner first.
- V2 means install, configure, activate and health-check, not just file synchronization.
- Other components remain on synchronization-oriented deployment until separately normalized.

## Repo artifacts introduced

- `contracts/deployment/deploy_contract_v2_tuner_first.md`
- `deploy/manifests/deploy_contract_v2_tuner_first.yaml`
- `deploy/v2/sr-deploy-v2.sh`
- `components/scale-radio-tuner/install.sh`
- `components/scale-radio-tuner/configure.sh`
- `components/scale-radio-tuner/healthcheck.sh`
- `components/scale-radio-tuner/runtime_manifest.yaml`

## Current practical state

The V2 flow is now structurally present in the repo, but it is not yet ready for a green deployment because the real tuner plugin payload still has to be imported into the Tuner component path.

That means the next high-value step is not more deployment theory, but importing the real tuner payload into the repo and then binding the install, configure and health-check hooks to the real runtime paths.
