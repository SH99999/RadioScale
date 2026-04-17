# STARTVERSION Contract Stack v1

## Purpose
This is the consolidated minimum operational contract set for RadioScale.

Goals:
- deterministic execution
- auditable changes
- team/agent operability
- minimal process overhead

## Scope
This stack is the **minimum active contract layer** for day-to-day work. Legacy contracts remain as history/reference unless explicitly re-activated.

## Active STARTVERSION contracts
- `contracts/repo/STARTVERSION_repo_operating_contract_v1.md`
- `contracts/deployment/STARTVERSION_deployment_contract_v1.md`
- `contracts/coding/STARTVERSION_coding_contract_v1.md`
- `contracts/gui/STARTVERSION_gui_contract_v1.md`
- `contracts/hardware/STARTVERSION_hardware_contract_v1.md`
- `contracts/observability/STARTVERSION_observability_contract_v1.md`
- `contracts/volumio4/STARTVERSION_volumio4_contract_v1.md`
- `contracts/integration-freeze/STARTVERSION_integration_freeze_contract_v1.md`

## Operating rule
If two rules conflict:
1. STARTVERSION file in the most specific folder wins.
2. Repo STARTVERSION wins over legacy repo contracts.
3. If still unclear, escalate to owner decision before merge.

## Audit minimum
Every PR using STARTVERSION must include:
- scope summary
- tests/checks executed
- rollback command
- owner decision required (`accept | changes-requested | reject`)
