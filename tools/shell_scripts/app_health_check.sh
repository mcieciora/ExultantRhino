#!/bin/bash

CHECK_TIME=$1
EXPECTED_VALUE=$2

docker compose -f docker-compose-local.yml up -d db
sleep 60
docker compose up -d
echo "Sleeping for $CHECK_TIME"
sleep "$CHECK_TIME"

VALUE=$(docker ps --format "{{.Names}}" | grep -c "exultant_rhino_*")

if [ "$VALUE" -eq "$EXPECTED_VALUE" ]; then
  exit 0
else
  echo "Found $VALUE running containers. Expected is $EXPECTED_VALUE."
  exit 1
fi
