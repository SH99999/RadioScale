# COMPONENT STATUS — system_integration_normalization

## 1. Scope
- component name: system_integration_normalization
- legacy names / aliases: SI/N, integration chat, normalization lane
- responsibility boundaries: branch doctrine, workflow model, deploy semantics, rollback semantics, repo governance, release-path normalization, cross-component integration policy
- non-goals: feature development inside specialist components, UI/UX implementation details, hardware logic implementation, source engine implementation

## 2. Current Functional Status
- what currently works:
  - `main` holds the active generic deploy/rollback workflows
  - repo-driven deployment works through `component-test-deploy-v6`
  - repo-driven rollback works through `component-test-rollback-v6`
  - bridge deploy lane is operational from `dev/bridge`
  - bridge rollback unregisters the plugin and restarts Volumio
  - branch cleanup doctrine is established and active branches were recently realigned close to `main`
- what partially works:
  - governance docs exist but placeholder cleanup is still being normalized by superseding v2 docs
  - journal structure exists but most component journals are not yet actively maintained
- what is broken:
  - no single fully mature journal stream discipline across all components yet
  - older placeholder docs/files still exist and should eventually be retired or replaced cleanly
- what was tested:
  - bridge deploy and rollback via v6 workflow on a real Pi
  - wrapper-free repo-driven execution path
- what is untested:
  - generic workflow support for non-bridge components
  - full CI enforcement beyond deploy/rollback reality

## 3. Repository Mapping
- correct component path in repo: `journals/system-integration-normalization/`
- correct payload path(s): none
- correct branch: `main` for truth; temporary fix branches only for repo-control-plane changes
- whether component belongs on main or dev branch right now: main

## 4. Locked Decisions
### DEC-SIN-01
- decision: `main` is the truth branch for workflows, governance, contracts, and accepted stable artifacts.
- rationale: operator-visible execution and repo doctrine need one canonical source.
- impact: workflows live on `main`; accepted stable artifacts may also live on `main`.

### DEC-SIN-02
- decision: component work happens on `dev/<component>` unless the component is stable enough for direct `main` truth.
- rationale: keeps unstable payload work separate while preserving one stable control plane.
- impact: bridge/fun-line/autoswitch/starter/hardware use dev branches; tuner is currently treated closer to main truth.

### DEC-SIN-03
- decision: deployment uses clean-replace semantics, not update-in-place.
- rationale: current system stability is not high enough for safe in-place plugin updates.
- impact: active runtime/config is removed or archived before installing a new payload.

### DEC-SIN-04
- decision: workflows must run from `main` and accept a selected `git_ref`.
- rationale: operator needs one visible Actions entrypoint while components continue to evolve on dev branches.
- impact: dual-checkout workflow model in v6.

### DEC-SIN-05
- decision: repo-driven wrapper logic is the only accepted deployment entrypoint model.
- rationale: stale Pi-local wrappers create drift and multi-Pi inconsistency.
- impact: wrapper is shipped in repo and invoked from workflow checkout, not trusted from target host state.

### DEC-SIN-06
- decision: rollback must unregister the plugin from Volumio when applicable.
- rationale: runtime path removal alone is insufficient for a clean operational rollback.
- impact: bridge rollback updates `/data/configuration/plugins.json` and restarts Volumio.

## 5. Open Decisions
- whether old placeholder v1 governance docs should be overwritten, deleted, or left as superseded stubs
- whether accepted stable component payloads beyond tuner should be promoted directly to `main`
- how strict CI enforcement should become in the next phase
- whether all component journals should be populated from legacy chats first or from repo reality first

## 6. Runtime / Deployment Notes
- install assumptions:
  - self-hosted Pi runner with labels matching workflow requirements
  - repo checkout available during workflow run
- uninstall / rollback assumptions:
  - active runtime path can be moved aside
  - Volumio restart and recovery check are required
- services:
  - `volumio`
  - `volumio-kiosk`
- configs:
  - component-specific paths under `/data/configuration/...`
  - Volumio plugin registration state in `/data/configuration/plugins.json`
- ports:
  - bridge overlay currently validated on `:5511`
- files / folders that matter:
  - `.github/workflows/component-test-deploy-v6.yml`
  - `.github/workflows/component-test-rollback-v6.yml`
  - `tools/deploy/sr-deploy-wrapper.sh`
  - component deploy candidate scripts under `components/<component>/deploy_candidates/`
- dependencies:
  - repo checkout on workflow runner
  - active component branch/payload
- activation behavior:
  - bridge may remain inactive after install and that is acceptable for now if runtime path and overlay work

## 7. Known Risks
- technical risks:
  - governance docs and journals may lag behind actual repo/runtime state
  - non-bridge components do not yet have the same mature deploy lane
- integration risks:
  - component branches drifting behind `main`
  - placeholder docs causing conflicting interpretations
- performance risks:
  - not yet centrally enforced
- rollback risks:
  - only bridge rollback path is currently well-validated

## 8. Next Recommended Steps
1. finish governance placeholder cleanup formally
2. populate real current-state and stream journals for all active components
3. add deploy candidate scripts for the next production-priority component after bridge/tuner
4. strengthen CI checks after journal/governance truth catches up

## 9. Hand-off Notes
A new specialist or integration chat should read the repo execution path, deployment decisions, release creation path, and the active v6 workflows first. The current system truth is repo-driven deployment from `main`, with selected component payloads taken from the chosen `git_ref`.
