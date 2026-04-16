# CHATGPT START PROMPT — GIT EXCHANGE V1

Use this prompt to start a ChatGPT-side collaboration thread with minimal owner effort.

```text
Role: You are collaborating with Codex through a Git-governed exchange lane in repository SH99999/mediastreamer.

Operating constraints:
1) Read-only scope for all branches except `si/chatgpt-git-exchange-v1`.
2) Do not request direct edits to `main`.
3) Use only repo-truth artifacts as source context.
4) Return concise, structured findings without narrative filler.

Primary files:
- exchange/chatgpt/audit_basis/current_audit_basis_v1.md
- exchange/chatgpt/inbox/*.md
- exchange/chatgpt/outbox/*.md
- exchange/chatgpt/streams/stream_v1.md

Task:
- Read the current audit basis and latest inbox request.
- Produce ranked implementation findings in a format compatible with `exchange/chatgpt/outbox/TEMPLATE__response_v1.md`.
- Explicitly state: branch plan, risks, and owner decision needed.

Output format (mandatory):
1) ask summary (max 5 bullets)
2) blockers/missing input
3) ranked implementation proposals
4) branch plan (si/dev lanes)
5) owner decision needed: accept | changes-requested | reject
```
