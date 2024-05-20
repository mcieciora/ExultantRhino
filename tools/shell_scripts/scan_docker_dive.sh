#!/bin/bash

DOCKERHUB_REPO="mcieciora/exultant_rhino"

TAGS="latest test_image"
for TAG in $TAGS; do
  echo "Running docker dive on $TAG image"
  docker run --rm -v /var/run/docker.sock:/var/run/docker.sock wagoodman/dive --ci $DOCKERHUB_REPO:"$TAG" > scan_dive_"$TAG".txt
done
