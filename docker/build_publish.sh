#!/bin/bash
set -e

clear
image_name="k2000_visa_generator"

version=$(python3 helpers/buildUtls.py get_version)
build_time=$(python3 helpers/buildUtls.py get_build_time)

docker build -f ../docker/Dockerfile --build-arg BUILD_VERSION=${version}  --build-arg BUILD_TIME=${build_time}  -t ${image_name}:latest ../.
echo


image_latest_name="${image_name}:latest"
image_version_name="${image_name}:${version}"

#git_repo="ghcr.io/robertolechowski"
#docker tag ${image_latest_name} ${git_repo}/${image_latest_name}
#docker tag ${image_latest_name} ${git_repo}/${image_version_name}

#docker push ${git_repo}/${image_latest_name}
#docker push ${git_repo}/${image_version_name}

echo
echo '=== DONE ==='
echo

$(python3 helpers/buildUtls.py inc_version)