#!/bin/bash

set -euo pipefail

cd "$(dirname "$0")/.."

version=$(python3 docker/build_utils.py inc_version)

git add docker/_ver.txt
git commit -m "release: ${version}"
git tag "${version}"
git push origin main "${version}"

repo="RobertOlechowski/k2000_visa_generator"
workflow="docker.yml"

echo "=========================================="
echo "Released ${version}"
echo ""
echo "GitHub Actions build started."
echo ""
echo "Status (browser):"
echo "  https://github.com/${repo}/actions/workflows/${workflow}"
echo ""
echo "Status (CLI):"
echo "  gh run watch --repo ${repo} --exit-status \$(gh run list --repo ${repo} --workflow ${workflow} --limit 1 --json databaseId --jq '.[0].databaseId')"
echo "=========================================="
