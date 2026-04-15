# OWNER OPERATIONAL REFERENCE V1

## Purpose
This page is the single owner-facing reference for daily operation, governance checks, onboarding shortcuts, click paths, and readiness decisions.

## Fast answer panel
### Are we ready to develop?
Use this YES/NO gate:
1. `main` is protected and PR-gated.
2. Agent bootstrap reports:
   - branch is `dev/<component>` or `si/<topic>`
   - remote `git` points to `https://github.com/SH99999/mediastreamer.git`
   - base sync is `ok`
   - push auth is `ok`
3. active issue/PR has governance labels.
4. affected component journal current-state + stream are updated.
5. deploy/rollback evidence is attached when runtime paths changed.

If any gate is `no`, treat as not ready and run the blocker path.

### Do we still have setup topics?
Current recurring topics to monitor:
- runtime token injection drift (`GH_TOKEN`/`GITHUB_TOKEN` not visible in active session)
- branch discipline drift (agents starting on `work` instead of `dev/*` or `si/*`)
- connector-lane mismatch (issue create available but PR create blocked, or vice versa)

### Can ChatGPT issue creation be automated?
Yes. Intake issue creation/normalization/routing is already automatable through repository workflows.
Use the issue templates and let workflows apply labels and routing automatically.
If connector write is blocked in a specific chat lane, fallback to PR-packaged intake fields and one-step owner handoff.

### Governance status
Governance model is operational for controlled branch->PR->main flow.
The remaining risk is runtime auth/connector availability, not missing governance doctrine.

## Owner daily flow (click-path version)
1. Open project board `Scale Radio Governance & Delivery`.
2. Check `Owner Decision Queue` view.
3. Open top item and read:
   - decision statement
   - options + recommended option
   - blocker or dependency notes
4. If accepted, approve PR to `main`.
5. Confirm post-merge checks:
   - rebase workflow run
   - decision/governance closeout comments
6. If blocked, request agent rerun with explicit owner action response.

## Minimal owner command checks (copy/paste)
```bash
bash tools/governance/agent_git_bootstrap_v1.sh
bash tools/governance/setup_auth_check_v1.sh
```
Interpretation:
- `push auth: ok` and `Auth check: result=ok` => agent can deliver branch+PR without owner push help.
- `blocked` => owner must fix runtime auth injection or perform final push/PR manually.

## When an agent says "Delivered to Git: NO"
Require this exact triage:
1. one blocker only
2. what is completed locally
3. one owner action only
4. no claim of pushed PR if push did not happen

## Primary links
### Governance and operating doctrine
- `AGENTS.md`
- `contracts/repo/system_integration_governance_index_v7.md`
- `contracts/repo/protected_main_truth_maintenance_operating_model_v1.md`
- `contracts/repo/deploy_process_standard_v1.md`
- `contracts/repo/ui_gui_governance_standard_v1.md`

### Owner onboarding and execution
- `docs/agents/system_integration_recovery_onboarding_v7.md`
- `docs/agents/agent_git_bootstrap_v1.md`
- `docs/agents/codex_cloud_environment_setup_v1.md`
- `docs/agents/container_startup_setup_v1.md`
- `docs/agents/chat_to_git_delivery_process_v1.md`
- `docs/agents/fallback_connector_blocked_manual_v1.md`

### Intake and decision automation
- `.github/ISSUE_TEMPLATE/governed-demand-intake.yml`
- `.github/ISSUE_TEMPLATE/ui-ux-and-asset-governance.yml`
- `.github/workflows/issue-intake-normalizer-v2.yml`
- `.github/workflows/system-integration-escalation.yml`
- `.github/workflows/open-decision-issues.yml`
- `.github/workflows/governance-closeout.yml`

### Owner project-view references
- `tools/governance/scale_radio_governance_delivery_views_v1.md`
- `tools/governance/scale_radio_governance_delivery_views_table_v1.md`
- `tools/governance/scale_radio_governance_delivery_views_kanban_v1.md`

## Required owner decision output format
When giving a decision back to agents, use:
- decision: `<accept|reject|defer>`
- scope: `<component(s) or governance topic>`
- mandatory follow-up: `<what must happen next>`
- merge authorization: `<yes|no>`

This keeps routing deterministic and minimizes follow-up clicks.
