#!/usr/bin/env bash
set -euo pipefail

BASE_BRANCH="${1:-main}"

if [[ -z "${GITHUB_HEAD_REF:-}" ]]; then
  echo "info: not running in pull_request context; skipping merge-clean check"
  exit 0
fi

git fetch origin "${BASE_BRANCH}" "${GITHUB_HEAD_REF}" --quiet

BASE_REF="origin/${BASE_BRANCH}"
HEAD_REF="origin/${GITHUB_HEAD_REF}"
BASE_HEAD_SHA="$(git rev-parse "${BASE_REF}")"
MERGE_BASE_SHA="$(git merge-base "${BASE_REF}" "${HEAD_REF}")"

if [[ "${BASE_HEAD_SHA}" != "${MERGE_BASE_SHA}" ]]; then
  echo "error: branch ${GITHUB_HEAD_REF} is not up to date with ${BASE_REF}"
  echo "action: Codex must rebase/refresh branch before PR is ready"
  exit 1
fi

WORKTREE_DIR="$(mktemp -d)"
cleanup() { rm -rf "${WORKTREE_DIR}"; }
trap cleanup EXIT

git worktree add -q "${WORKTREE_DIR}" "${HEAD_REF}"
pushd "${WORKTREE_DIR}" >/dev/null

if ! git merge --no-commit --no-ff "${BASE_REF}" >/dev/null 2>&1; then
  echo "error: merge conflicts detected against ${BASE_REF}"
  echo "action: Codex must resolve conflicts before PR readiness"
  exit 1
fi

git merge --abort >/dev/null 2>&1 || true
popd >/dev/null

echo "ok: PR branch is up to date with ${BASE_REF} and merge-clean"
