# COMPONENT STATUS — system_integration_normalization

Status note: this v4 file supersedes the earlier v3 snapshot as the current intake-specific SI/N status addendum.

## Intake correction summary
- canonical component root paths use the full governed component name
- canonical journal paths use the full governed component name
- long-lived work branches use the component suffix token
- the corrected standard is `contracts/repo/new_component_intake_standard_v2.md`

## Example mapping
- component name: `scale-radio-bridge`
- component root: `components/scale-radio-bridge/`
- journals: `journals/scale-radio-bridge/`
- work branch: `dev/bridge`

## Current rule
- new components should bootstrap through one bundled PR to protected `main`
- after merge, ongoing work continues on `dev/<component-suffix>`
- future chats should use the corrected standard and not the older ambiguous wording

## Follow-up note
This v4 status addendum exists because Codex correctly identified ambiguity in the earlier intake wording. The corrected standard and this status note remove that ambiguity for future component creation.
