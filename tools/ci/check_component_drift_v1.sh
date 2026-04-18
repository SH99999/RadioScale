#!/usr/bin/env bash
set -euo pipefail

MAX_BEHIND="${MAX_BEHIND:-50}"

git fetch origin main 'dev/*' --quiet

main_sha="$(git rev-parse origin/main)"
fail=0

while IFS= read -r ref; do
  branch="${ref#origin/}"
  behind="$(git rev-list --count "${ref}..origin/main")"
  ahead="$(git rev-list --count "origin/main..${ref}")"
  echo "${branch}: behind=${behind} ahead=${ahead}"
  if (( behind > MAX_BEHIND )); then
    echo "error: ${branch} drift exceeds MAX_BEHIND=${MAX_BEHIND}"
    fail=1
  fi
  # if branch has no common base (extreme case), mark fail
  if ! git merge-base --is-ancestor "$(git merge-base "${ref}" origin/main)" "${main_sha}"; then
    echo "error: ${branch} merge-base check failed"
    fail=1
  fi
done < <(git for-each-ref --format='%(refname:short)' refs/remotes/origin/dev/)

if (( fail )); then
  echo "action: Codex must refresh/rebase drifted component branches."
  exit 1
fi

echo "ok: component branch drift within threshold"
