#!/usr/bin/env bash
# Applies one of the prepared breakages on a new branch and opens a pull request,
# so failtriage has a failing run to report on. Needs git and an authenticated gh.
set -euo pipefail
cd "$(git rev-parse --show-toplevel)"

name=${1:-}
if [ -z "$name" ] || [ ! -f "demos/$name.patch" ]; then
  echo "usage: scripts/demo.sh <name>, where name is one of:" >&2
  for patch in demos/*.patch; do
    basename "$patch" .patch >&2
  done
  exit 2
fi
if [ -n "$(git status --porcelain)" ]; then
  echo "commit or stash your changes first" >&2
  exit 1
fi

base=$(git symbolic-ref --short HEAD)
message=$(cat "demos/$name.msg")
git checkout -b "demo/$name"
git apply "demos/$name.patch"
git commit -qam "$message"
git push -u origin "demo/$name"
gh pr create --base "$base" --head "demo/$name" --title "$message" \
  --body "Opened by scripts/demo.sh to try failtriage."
