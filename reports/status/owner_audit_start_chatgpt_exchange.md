# Owner Report — ChatGPT Audit Start (Exchange)

## Purpose
Single owner-facing entry for starting the ChatGPT↔Codex audit loop with minimal clicks.

## Canonical start prompt
Use this file as source of truth:
- `docs/agents/chatgpt_start_prompt_git_exchange_v3.md`

## Quick start
1. Start ChatGPT with prompt v3.
2. Ensure first artifact completed is:
   - `exchange/chatgpt/audit_basis/current_audit_basis_v1.md`
3. Wait for status marker:
   - `status: ready-for-codex`
4. Codex validates and prepares owner decision packet:
   - `exchange/chatgpt/outbox/<topic>__owner_decision_packet_v1.md`

## Owner expected handoff
- human-readable decision packet only
- recommendation + risk + rollback + next click

## Next owner click
- `accept | changes-requested | reject`
