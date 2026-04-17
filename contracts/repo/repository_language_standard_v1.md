# REPOSITORY LANGUAGE STANDARD V1 — MINIMUM OPERATING VERSION (vMIN.1)

Status: active minimum baseline for RadioScale.
Source lineage: `mediastreamer/contracts/repo/repository_language_standard_v1.md`.
Last normalized: 2026-04-17.

## Purpose
Define only the minimum deterministic rules required to operate safely and auditable.

## Minimum deterministic rules
1. **Single truth branch**: `main` is protected truth; implementation happens on non-`main` branches.
2. **PR-gated change**: every truth mutation requires branch + PR + owner merge decision.
3. **Explicit state**: each execution-relevant change records actor, target, inputs, result, and timestamp.
4. **Rollback-first safety**: any operation with runtime impact must provide rollback action or explicit blocker.
5. **No implicit behavior**: commands, statuses, and transitions must be written as concrete allowed values.

## Required evidence (minimum)
- `who`: responsible role or agent id
- `what`: exact artifact/path changed
- `where`: branch/ref and repo path
- `when`: UTC timestamp
- `result`: pass/fail/blocked
- `rollback`: command/path or `not-applicable`

## Audit & handoff
- Keep entries concise and factual.
- Prefer machine-checkable fields where possible.
- If execution is blocked, record blocker explicitly instead of inferring success.

## Out of scope
- Narrative process expansion
- Duplicate authority chains
- Non-deterministic owner instructions
