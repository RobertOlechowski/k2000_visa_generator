#!/bin/bash

set -euo pipefail

IMAGE_NAME="${1:-k2000-visa-generator}"
REPO_NAME="ghcr.io/robertolechowski"
LOG_FILE="docker/build.log"

# Run from project root
cd "$(dirname "$0")/.."

version=$(python3 docker/build_utils.py get_version)
build_time=$(python3 docker/build_utils.py get_build_time)
build_revision=$(git rev-parse HEAD)

export DOCKER_BUILDKIT=1

echo "--- Build started at $(date) ---" > "$LOG_FILE"
echo "=========================================="
echo "Image:   ${IMAGE_NAME}:latest"
echo "Version: ${version}"
echo "Log:     ${LOG_FILE}"
echo "=========================================="

if ! docker build --platform linux/amd64 --progress=plain -f docker/Dockerfile \
    --build-arg BUILD_VERSION="${version}" \
    --build-arg BUILD_TIME="${build_time}" \
    --build-arg BUILD_REVISION="${build_revision}" \
    -t "${IMAGE_NAME}:latest" . 2>&1 | tee -a "$LOG_FILE"; then
    echo "==========================================" | tee -a "$LOG_FILE" >&2
    echo "Docker build failed. See ${LOG_FILE} for details." | tee -a "$LOG_FILE" >&2
    echo "==========================================" | tee -a "$LOG_FILE" >&2
    exit 1
fi

docker tag "${IMAGE_NAME}:latest" "${REPO_NAME}/${IMAGE_NAME}:latest"
docker tag "${IMAGE_NAME}:latest" "${REPO_NAME}/${IMAGE_NAME}:${version}"

echo "=========================================="
echo "Image ${IMAGE_NAME}:latest"
echo "Image ${IMAGE_NAME}:${version}"
echo "Next Version: $(python3 docker/build_utils.py inc_version)"
echo "=========================================="
echo ""
echo "Run:"
echo "  docker run --rm -p 5000:5000 ${IMAGE_NAME}:latest"
echo "  docker push ${REPO_NAME}/${IMAGE_NAME}:latest"
echo "  docker push ${REPO_NAME}/${IMAGE_NAME}:${version}"
