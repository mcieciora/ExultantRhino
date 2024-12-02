#!/bin/bash

DOCKERHUB_REPO="mcieciora/exultant_rhino"

TAGS="latest test_image"
for TAG in $TAGS; do
  echo "Running docker dive on $TAG image"
  docker run --rm -v /var/run/docker.sock:/var/run/docker.sock wagoodman/dive --ci $DOCKERHUB_REPO:"$TAG" > scan_dive_"$TAG".txt
  grep "Failed:0" scan_dive_"$TAG".txt
  HIGH_VULNERABILITIES=$?
  grep "Failed:0" scan_dive_"$TAG".txt
  CRITICAL_VULNERABILITIES=$?
  if [ "$HIGH_VULNERABILITIES" -ne 0 ] || [ "$CRITICAL_VULNERABILITIES" -ne 0 ]; then
    echo "Script failed, because vulnerabilities were found. Please fix them according to given recommendations."
  fi
done
