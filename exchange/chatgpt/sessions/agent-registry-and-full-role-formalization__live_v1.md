# agent-registry-and-full-role-formalization live v1

status: live
actor: chatgpt

## source/context
- source chat/session: current governed ChatGPT session with owner
- source timestamp (UTC): 2026-04-17T00:00:00Z
- participants: owner, chatgpt

## current objective
- formalize the full agent landscape in repo truth so SI knows which agents exist, which are available, and which can receive delegated work
- make agent startup deterministic for Codex through canonical role descriptions, startup prompts, and bootstrap commands
- let owner inspect defined agents, availability, role descriptions, startup prompt paths, and bootstrap commands from Git truth

## locked decisions so far
1. `dev-fun-line`, `dev-autoswitch`, `dev-ux`, and `dev-hardware` should be available as formal agent roles
2. the role/delegation model must be captured in governance and SI delegation logic must read from repo truth rather than implicit memory
3. owner must be able to inspect which agents are defined, whether they are available, what their role is, which startup prompt is correct, and which bootstrap command should be used
4. hardware is a required first-class role and must not remain only a routing/component concept
5. startup/bootstrap helpers for Codex should be added so agent creation/launch is easier and deterministic

## open decisions
1. whether additional optional roles beyond the requested set should be marked `planned` in the first registry version if they are not actively used now

## active implementation asks
1. add a canonical agent registry in human-readable and machine-readable form
2. extend role/startup/bootstrap materials to include hardware, fun-line, autoswitch, and ux as first-class roles
3. update SI-facing delegation guidance so SI reads available roles from repo truth
4. add owner-visible startup index and links so owner can inspect/start agents with minimal friction

## active risks/blockers
1. current repo state formalizes only SI, tuner, bridge, and generic startup roles cleanly; other desired roles risk remaining implicit if not registered centrally
2. SI cannot safely delegate by repo truth if available/unavailable roles are not centralized
3. owner friction remains too high if startup paths and role availability stay scattered across multiple docs

## non-loss requirements
1. the requested agent roster and role expectations from this chat must not remain only in chat memory
2. any canonical registry must remain compatible with existing AGENTS/bootstrap/role-profile/start-prompt structure
3. owner must not need to reverse-engineer role availability from labels or streams

## current lifecycle status
- live

## last material update timestamp
- 2026-04-17T00:00:00Z
