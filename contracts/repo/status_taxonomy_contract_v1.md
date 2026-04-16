# STATUS TAXONOMY CONTRACT V1

## Purpose
This contract defines the canonical lifecycle status vocabulary for component and release reporting.

## Leading rule
- Use only canonical statuses in journals, status pages, workflow outputs, and owner decision packets.
- Legacy statuses may be ingested temporarily but must be normalized through the migration map in this document.

## Canonical statuses (ordered)
1. `raw_intake_started`
2. `payload_partial`
3. `payload_complete`
4. `deployment_candidate_started`
5. `deploy_ready`
6. `tested_on_pi`
7. `functional_acceptance_open`
8. `accepted_for_main`
9. `rolled_back`
10. `superseded`

## Canonical status definitions
### `raw_intake_started`
Release material entered the repository and the target branch/path is known.

### `payload_partial`
Payload tree exists but completeness or correctness is not yet trusted.

### `payload_complete`
Expected payload structure is present and core runtime files are in place.

### `deployment_candidate_started`
Deploy, healthcheck, and rollback scripts exist or are actively being prepared.

### `deploy_ready`
The repository-driven workflow can install and remove the payload using clean-replace semantics.

### `tested_on_pi`
Deploy and/or rollback ran on a real Pi through the active workflow lane.

### `functional_acceptance_open`
Deployment path works, but component-level feature acceptance is still open.

### `accepted_for_main`
The payload is stable enough to be treated as current truth on `main`.

### `rolled_back`
The active deployment was removed, unregistered when applicable, and recovery was verified.

### `superseded`
The release remains in history only and is no longer the active accepted candidate.

## Migration map (legacy -> canonical)
- `payload_present` -> `payload_partial`
- `deploy_candidate_started` -> `deployment_candidate_started`
- `functional_acceptance_pending` -> `functional_acceptance_open`
- `placeholder` -> `raw_intake_started` (if intake started) or keep outside lifecycle as non-release marker

## Reporting rules
- status generators should emit canonical values only
- if a legacy status is detected, normalize using the migration map and log the normalized value
- when unknown values appear, fail fast with explicit remediation text
