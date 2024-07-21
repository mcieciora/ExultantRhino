#!/bin/bash

DOCKERHUB_REPO="mcieciora/exultant_rhino"

TAGS="latest test_image"
for TAG in $TAGS; do
  echo "Running docker trivy on $TAG image"
  docker run --rm aquasec/trivy image $DOCKERHUB_REPO:"$TAG" > scan_trivy_"$TAG".txt
done
