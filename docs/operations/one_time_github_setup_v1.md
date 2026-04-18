# One-time GitHub setup (simple)

Do this once. After this, normal delivery should run without recurring owner maintenance.

## 1) Protect `main`
1. Open GitHub repository `SH99999/RadioScale`.
2. Click **Settings**.
3. Click **Branches**.
4. Under **Branch protection rules**, click **Add rule**.
5. In **Branch name pattern**, type `main`.
6. Turn on **Require a pull request before merging**.
7. Turn on **Require status checks to pass before merging**.
8. In status checks, add:
   - `ci-shell-syntax-v1`
   - `pr-merge-clean-v1`
9. Turn on **Require branches to be up to date before merging**.
10. Click **Create** or **Save changes**.

## 2) Create archive branch `ops/chat-archive`
1. Open **Code** tab.
2. Click branch selector (usually says `main`).
3. Type `ops/chat-archive` and click **Create branch: ops/chat-archive**.
4. On that branch, create folders:
   - `handoff/open/`
   - `handoff/assets/`
   - `handoff/closed/`
5. Commit once on `ops/chat-archive`.

## 3) Rule reminder
- `ops/chat-archive` is archive/input only.
- Never merge `ops/chat-archive` into `main`.
