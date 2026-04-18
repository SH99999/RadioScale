#!/usr/bin/env bash
set -euo pipefail

EXCLUDE_BRANCHES="${EXCLUDE_BRANCHES:-}"

is_excluded() {
  local b="$1"
  for x in ${EXCLUDE_BRANCHES}; do
    [[ "$b" == "$x" ]] && return 0
  done
  return 1
}

git fetch origin main '+refs/heads/dev/*:refs/remotes/origin/dev/*' --quiet

while IFS= read -r ref; do
  branch="${ref#origin/}"

  if is_excluded "$branch"; then
    echo "skip excluded: $branch"
    continue
  fi

  echo "refresh: $branch"
  git checkout -B "$branch" "$ref" >/dev/null 2>&1

  if git merge --no-edit origin/main >/dev/null 2>&1; then
    git push origin "$branch"
    echo "ok: $branch refreshed"
  else
    git merge --abort >/dev/null 2>&1 || true
    echo "error: merge conflict while refreshing $branch"
    exit 1
  fi
done < <(git for-each-ref --format='%(refname:short)' refs/remotes/origin/dev/)
