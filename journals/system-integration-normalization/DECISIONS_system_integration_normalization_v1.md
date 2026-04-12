# DECISION LOG — system_integration_normalization

## Decision Entries

### DEC-system_integration_normalization-01
- Status: locked
- Decision: `main` is the canonical truth branch for workflows, governance, contracts, and accepted stable artifacts.
- Date context: established during repository normalization phase
- Why this was chosen: one operator-visible control plane is required to avoid branch and workflow ambiguity.
- What it affects: workflow placement, governance docs, accepted stable payload promotion.
- What it explicitly does NOT affect: whether unstable component work may continue on `dev/*` branches.
- Follow-up needed: keep branch doctrine wording consistent across docs.

### DEC-system_integration_normalization-02
- Status: locked
- Decision: active component work belongs on `dev/<component>` unless the component is already stable enough for `main` truth.
- Date context: branch cleanup and normalization phase
- Why this was chosen: separates unstable work from stable operator-facing repo truth.
- What it affects: branch selection for bridge, fun-line, autoswitch, starter, hardware, and similar lanes.
- What it explicitly does NOT affect: tuner or other components that are intentionally promoted to `main` truth.
- Follow-up needed: keep all active `dev/*` branches at `0 behind main`.

### DEC-system_integration_normalization-03
- Status: locked
- Decision: deployment uses clean-replace semantics, not update-in-place semantics.
- Date context: early bridge deployment governance
- Why this was chosen: current plugin/runtime stability is not high enough for safe in-place updates.
- What it affects: deploy candidate scripts, rollback logic, payload install behavior.
- What it explicitly does NOT affect: future possibility of update-in-place once stability is proven.
- Follow-up needed: encode this in all new component deploy candidate scripts.

### DEC-system_integration_normalization-04
- Status: locked
- Decision: workflows must live on `main` and accept a selected `git_ref`.
- Date context: first manual workflow visibility fix
- Why this was chosen: GitHub manual workflows are operator-friendly when visible on the default branch.
- What it affects: all manual deploy and rollback workflows.
- What it explicitly does NOT affect: where component payloads live.
- Follow-up needed: keep only the current supported workflow generation visible.

### DEC-system_integration_normalization-05
- Status: locked
- Decision: the repo-shipped wrapper is the only accepted deployment entrypoint model.
- Date context: stale Pi-local wrapper mismatch investigation
- Why this was chosen: multi-Pi consistency requires the repo to ship the execution model.
- What it affects: `tools/deploy/sr-deploy-wrapper.sh`, v6 workflow model.
- What it explicitly does NOT affect: legacy Pi-local wrappers already installed; those should simply no longer be trusted.
- Follow-up needed: extend wrapper support beyond bridge.

### DEC-system_integration_normalization-06
- Status: locked
- Decision: rollback must also unregister the plugin in Volumio when relevant.
- Date context: bridge rollback hardening
- Why this was chosen: removing files without unregistering plugin state leaves operational residue.
- What it affects: bridge rollback logic and future plugin rollback paths.
- What it explicitly does NOT affect: non-plugin components that have no Volumio plugin registration.
- Follow-up needed: apply same principle to future plugin-based components.

### DEC-system_integration_normalization-07
- Status: locked
- Decision: bridge may remain inactive after install for now if runtime deployment, overlay reachability, and rollback are working.
- Date context: validated bridge deploy tests
- Why this was chosen: runtime path and overlay proved operational even though Volumio activation state is not yet ideal.
- What it affects: current bridge acceptance threshold.
- What it explicitly does NOT affect: future expectation of better activation behavior.
- Follow-up needed: keep documenting this as a known acceptable temporary state.

## Superseded Decisions
- None formally recorded yet in repo decision-log format.
