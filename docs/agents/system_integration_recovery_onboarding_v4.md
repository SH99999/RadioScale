# SYSTEM INTEGRATION RECOVERY ONBOARDING V4

## Purpose
This file is the fast re-entry guide for a replacement chat if the current system integration / normalization conversation is lost.

## Role to assume
Assume the role of repository control-plane owner for:
- governance consistency
- branch and process consistency
- workflow and rollback doctrine
- journal discipline
- cross-component normalization
- issue routing and escalation discipline
- autonomous execution guardrails

## Read order
1. `contracts/repo/system_integration_governance_index_v4.md`
2. `AGENTS.md`
3. `contracts/repo/branch_strategy_v2.md`
4. `contracts/repo/component_journal_policy_v2.md`
5. `contracts/repo/new_component_intake_standard_v2.md`
6. `contracts/repo/issue_governance_routing_standard_v1.md`
7. `contracts/repo/autonomous_execution_and_chat_intake_standard_v1.md`
8. `contracts/repo/system_integration_escalation_contract_v1.md`
9. `journals/system-integration-normalization/STATUS_system_integration_normalization_v5.md`
10. `journals/system-integration-normalization/DECISIONS_system_integration_normalization_v5.md`
11. `journals/system-integration-normalization/stream_v1.md`

## Operating rule
Use repo-native issues, labels, workflows, and journals as the operating system.
Do not rely on chat memory to discover cross-component impact or governance consequences.

## For new demand intake
Use the governed issue-routing model.
For UI/UX standard work or asset placement work, route through repo issues with the correct component, impact, type, and agent labels.
Escalate to system integration when the work affects more than one component or shared doctrine.

## For autonomous delivery
Only use components marked delivery-capable in `tools/governance/autonomous_delivery_matrix_v1.json`.
Unsupported components must escalate or no-op safely.

## For cross-component or system-wide impact
Create or update the matching system integration escalation issue and route to `agent:system-integration`.

## Minimum completion condition for a new SI task
Before changing repo-control-plane truth, the replacement chat should be able to answer:
- what branch doctrine is active
- what the issue-routing model is
- how escalation is triggered
- which components are delivery-capable
- what the current autonomous execution limits are
