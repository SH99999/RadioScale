# STARTVERSION Contract Stack v1

## Purpose
Minimum RadioScale contract set for deterministic, auditable, low-admin execution.

## Canonical operating source
- `contracts/repo/STARTVERSION_repo_operating_contract_v1.md`

## Active contracts
- `contracts/deployment/STARTVERSION_deployment_contract_v1.md`
- `contracts/coding/STARTVERSION_coding_contract_v1.md`
- `contracts/gui/STARTVERSION_gui_contract_v1.md`
- `contracts/hardware/STARTVERSION_hardware_contract_v1.md`
- `contracts/observability/STARTVERSION_observability_contract_v1.md`
- `contracts/volumio4/STARTVERSION_volumio4_contract_v1.md`
- `contracts/integration-freeze/STARTVERSION_integration_freeze_contract_v1.md`
- `contracts/integrations/chatgpt_v1.md`

## Conflict rule
1. Repo operating contract is the root authority.
2. More specific contract wins if not conflicting.
3. If still unclear, escalate once to owner.

## PR minimum
- scope summary
- executed checks
- rollback command
- owner decision (`accept | changes-requested | reject`)
