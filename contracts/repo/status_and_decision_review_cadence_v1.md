# STATUS AND DECISION REVIEW CADENCE V1

## Purpose
This cadence keeps current-state journals, stream journals, and decision logs alive enough for active development.

## Leading rule
Status and decisions are not archival paperwork. They are active operating documents.

## Minimum cadence
### On every meaningful change
Update at least:
- component `stream_v1.md`
- component `current_state_v1.md` if the operational reality changed

Meaningful change includes:
- new accepted baseline
- deploy or rollback validation result
- component path normalization
- technology-shape change
- important risk discovered
- promotion or demotion of a branch/baseline

### Weekly integration review
At least once per active week, integration should review:
- components with unresolved repo-truth uncertainty
- components whose `current_state_v1.md` still says `payload_partial`
- components with open technology-shape questions
- components with stale baselines or missing validation

### Before promotion to main truth
Before treating a component baseline as current truth, verify:
- current_state is updated
- stream is updated
- README matches the same truth
- decision log reflects any newly locked decision

## Triggered review cases
A forced review is required when:
- a component changes technology shape
- a component adds/removes artifacts
- a component changes rollback anchor
- a component changes deploy entrypoint
- a component moves from dev-only toward main-truth readiness

## Ownership
- specialist chat: proposes component reality
- integration chat: normalizes repo truth and cross-component consistency
- operator: validates runtime/deploy results on target Pi

## Practical rule for speed
If time is tight:
- update stream first
- update current_state second
- update decision log only when a choice is actually locked
