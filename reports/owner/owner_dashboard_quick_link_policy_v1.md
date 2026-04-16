# Owner Dashboard Quick Link Policy v1

## Decision
Any newly created owner-critical document MUST be linked from `reports/owner/owner_dashboard_v1.html` in the same change set.

## Owner-critical scope
- start prompts (ChatGPT/agents)
- owner decision packets and owner-start reports
- governance proof reports
- kanban/project decision links
- high-priority runbooks needed for one-click decisions

## Enforcement rule (process)
- PR is not ready for merge if an owner-critical document was added but dashboard link was not added.
