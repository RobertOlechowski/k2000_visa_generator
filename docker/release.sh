#!/bin/bash

set -euo pipefail

cd "$(dirname "$0")/.."

if ! git diff --quiet || ! git diff --cached --quiet; then
  echo "ERROR: Uncommitted changes detected. Commit or stash them before releasing." >&2
  git status --short >&2
  exit 1
fi

if [ -n "$(git ls-files --others --exclude-standard)" ]; then
  echo "ERROR: Untracked files detected. Commit or remove them before releasing." >&2
  git ls-files --others --exclude-standard >&2
  exit 1
fi

version=$(python3 docker/build_utils.py inc_version)

git add docker/_ver.txt
git commit -m "release: ${version}"
git tag "${version}"
git push origin main "${version}"

repo="RobertOlechowski/k2000_visa_generator"
run_id=$(gh run list --repo "${repo}" --limit 1 --json databaseId --jq '.[0].databaseId' 2>/dev/null || echo "")

echo "=========================================="
echo "Released ${version}"
echo ""
echo "GitHub Actions build started."
echo ""
if [ -n "${run_id}" ]; then
  echo "Status:  https://github.com/${repo}/actions/runs/${run_id}"
  echo "Logs:    https://github.com/${repo}/actions/runs/${run_id}?pr="
  echo ""
  echo "  gh run watch ${run_id}"
  echo "  gh run view  ${run_id} --log-failed"
else
  echo "  gh run list --repo ${repo} --limit 5"
  echo "  gh run view <run_id> --log-failed"
fi
echo "=========================================="
