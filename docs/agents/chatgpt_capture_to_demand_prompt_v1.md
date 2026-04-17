# ChatGPT capture-to-demand prompt v1

## Purpose
Provide a one-time activation prompt so repo-relevant chats persist live state to Git and route to Codex with minimal owner repetition.

## One-time activation prompt
Use this once at the beginning of a repo-relevant chat:

```text
governed mode on
Topic: <topic>
Open or create live session artifact at exchange/chatgpt/sessions/<topic>__live_v1.md.
From now on, persist every material decision/request/risk/blocker/non-loss delta to that live session within 5 minutes.
When context is execution-ready, run chatok promotion to exchange/chatgpt/demands/<topic>__intake_v1.md and set demand status to ready-for-codex.
After codex output is prepared, require ready-for-chatgpt-review -> pre-ok before ready-for-owner.
Keep owner commands minimal: governed mode on | chatok | ship to codex | close demand.
```

## Command semantics
- `governed mode on`: activates live Git continuity for the chat.
- `chatok`: lock/promote live session into a demand intake.
- `ship to codex`: ensure demand is `ready-for-codex` and watcher-visible.
- `close demand`: set lifecycle to `closed` after owner decision path completes.

## Required outputs from a governed chat
1. live session artifact path
2. demand intake path
3. PR link (when implementation exists)
4. rollback command
5. next owner click
