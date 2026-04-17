# STARTVERSION Repo Operating Contract v1

## 1) Branch and truth model
- `main` is protected canonical truth.
- Never commit directly to `main`.
- Use dedicated work branches:
  - `si/<topic>` for system integration/governance/repo-control-plane
  - `dev/<component>` for component work
- Do not use ambiguous branch names (e.g., `work`).

## 2) Delivery model
- Work is executed via PRs to `main`.
- Keep PRs narrow and reversible.
- No parallel truth chains outside Git.

## 3) Chat intake and execution
- Chat intent becomes repo truth before implementation (demand/protocol/inbox flow).
- Codex executes from repo truth, not chat memory.
- If a required artifact is missing, stop and report the exact missing artifact.

## 4) Ownership and delegation
- Owner decides at PR gate.
- SI orchestrates routing, dependencies, and package sequencing.
- Delegate only to agents marked available in agent registry.

## 5) Minimal mandatory artifacts per package
- branch
- commit(s)
- PR
- test/check outputs
- rollback command

## 6) Non-negotiables
- No dashboard/board/html sprawl for governance control.
- No hidden side channels for approvals.
- No fake-success reporting.
