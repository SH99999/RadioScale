# NAMING AND RELEASE NUMBERING STANDARD V1

## Purpose
This contract makes naming and release numbering mandatory and repository-wide.

## Leading rules
- repository-facing naming is English
- component names are normalized and stable
- new governed releases use a predictable numbering model
- ad-hoc release names are not the default for new normalized work

## Component naming
Repository component directories must use this form:
- `components/scale-radio-<component>/`

Examples:
- `components/scale-radio-bridge/`
- `components/scale-radio-tuner/`
- `components/scale-radio-autoswitch/`

Legacy aliases may be recorded in journals or docs, but the normalized repo name remains the canonical name.

## Branch naming
Use:
- `main`
- `integration/staging`
- `dev/<component>`

Examples:
- `dev/bridge`
- `dev/tuner`
- `dev/fun-line`

## Artifact naming
When a component contains multiple artifacts, artifact names should reflect the component plus the artifact role.

Preferred pattern inside docs/manifests:
- `<component>:<artifact_role>`

Examples:
- `bridge:runtime`
- `bridge:launcher`
- `tuner:runtime`
- `tuner:source_tile`

## Payload directory naming
### Mutable working payloads
Use these reserved names only:
- `current_dev` = current development payload on a component branch
- `current` = current accepted payload when that is the intentionally maintained pointer

### Immutable numbered releases
New normalized governed releases should use:
- `vMAJOR.MINOR.PATCH`

Examples:
- `v0.1.0`
- `v1.0.0`
- `v1.2.3`

## Release numbering model
Use semantic versioning at the component release level:
- `MAJOR` = incompatible contract or deployment change
- `MINOR` = backward-compatible feature or artifact expansion
- `PATCH` = backward-compatible fix or packaging correction

## Multi-artifact release rule
If multiple artifacts belong to one component, they normally share the **same component release number**.

Example:
- `bridge:runtime` and `bridge:launcher` both belong to component release `v1.3.0`

Do not invent separate artifact version lines unless governance explicitly documents that split.

## Historical imports
Previously imported payload names such as legacy stable tags or descriptive folder names may remain for historical continuity.
However:
- they should be marked as historical or pre-normalization where relevant
- new normalized releases should use the standard numbering model

## Required release handoff fields
Every governed release handoff should state:
- component name
- branch/ref
- payload path
- release number or reserved mutable pointer name
- artifact roles included in that release
- current lifecycle status

## Enforcement intention
This naming and release numbering standard should be treated as mandatory governance and should be enforced by CI progressively.
