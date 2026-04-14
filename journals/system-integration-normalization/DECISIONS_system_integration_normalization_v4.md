# DECISION LOG — system_integration_normalization

Status note: this v4 file supersedes the earlier v3 snapshot as the current repo-facing SI/N decision log.

## Decision Entries

### DEC-system_integration_normalization-10
- Status: locked
- Decision: new components must use the corrected bootstrap path recorded in `contracts/repo/new_component_intake_standard_v2.md`.
- Date context: component intake hardening phase
- Why this was chosen: future component creation needs one repeatable path that preserves branch, path, and journal discipline.
- What it affects: component creation, root paths, journals, and branch setup.
- What it explicitly does NOT affect: later specialist work inside an already bootstrapped component.
- Follow-up needed: use this corrected standard for future component creation.

### DEC-system_integration_normalization-11
- Status: locked
- Decision: low-click operation means bundling bootstrap setup into one clean PR while keeping `main` protected.
- Date context: component intake hardening phase
- Why this was chosen: the repo needs strong truth control without high review friction.
- What it affects: how new-component setup work is packaged and presented for review.
- What it explicitly does NOT affect: the need for later PRs when real component work continues.
- Follow-up needed: keep bootstrap PRs bundled and concise.

### DEC-system_integration_normalization-12
- Status: locked
- Decision: component root and journal paths use the full canonical component name, while the long-lived work branch uses the component suffix.
- Date context: follow-up correction after path and branch ambiguity review
- Why this was chosen: path naming and branch naming must each use one token consistently to avoid drift.
- What it affects: component bootstrap paths and branch naming.
- What it explicitly does NOT affect: existing governed component names already in canonical form.
- Follow-up needed: keep future bootstrap docs aligned with this mapping.

## Superseded Decisions
- The earlier v3 decision-log file remains a historical snapshot, while this v4 file becomes the current intake-specific operating addendum.
