#!/bin/bash

RETURN_VALUE=0
DOCKERHUB_REPO="mcieciora/careless_vaquita"

TAGS="latest test_image"
for TAG in $TAGS; do
  echo "Running docker scout on $TAG image"
  docker scout cves $DOCKERHUB_REPO:"$TAG" --exit-code --only-severity critical,high
  SCAN_RESULT=$?
  if [ "$SCAN_RESULT" -ne 0 ]; then
    echo "Vulnerabilities found. Running recommendations"
    docker scout recommendations $DOCKERHUB_REPO:"$TAG" > scan_"$TAG".txt
    grep "This image version is up to date" scan_"$TAG".txt
    IMAGE_UP_TO_DATE=$?
    grep "There are no tag recommendations at this time" scan_"$TAG".txt
    RECOMMENDATIONS_AVAILABLE=$?
    if [ "$IMAGE_UP_TO_DATE" -eq 0 ] && [ "$RECOMMENDATIONS_AVAILABLE" -eq 0 ] && [ "$RETURN_VALUE" -ne 1 ]; then
      RETURN_VALUE=0
    else
      RETURN_VALUE=1
    fi
  else
    echo "No vulnerabilities detected"
  fi
done

exit "$RETURN_VALUE"
