# One-time GitHub setup

Do this once.

## Protect `main`
1. Open repository `SH99999/RadioScale`.
2. Click **Settings**.
3. Click **Branches**.
4. Click **Add rule**.
5. Set branch name pattern to `main`.
6. Enable **Require a pull request before merging**.
7. Enable **Require status checks to pass before merging**.
8. Add required checks:
   - `ci-shell-syntax-v1`
   - `pr-merge-clean-v1`
9. Enable **Require branches to be up to date before merging**.
10. Click **Save changes**.

## Create archive branch
1. Go to **Code**.
2. Open the branch selector.
3. Type `ops/chat-archive` and create it.
4. On `ops/chat-archive`, create:
   - `handoff/open/`
   - `handoff/assets/`
   - `handoff/closed/`
5. Commit once on `ops/chat-archive`.

`ops/chat-archive` is archive/input only and is never merged into `main`.
