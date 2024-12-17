FROM --platform="${TARGETPLATFORM:-linux/amd64}" python:3.12.2-slim

RUN apt-get update && apt-get install -y libpq-dev gcc firefox-esr

WORKDIR /app
COPY requirements /app/requirements
COPY pytest.ini ./

WORKDIR /app/automated_tests
COPY automated_tests .

WORKDIR /app/src
COPY src .

WORKDIR /app/tools/python
COPY tools/python .

WORKDIR /app
RUN python -m pip install --no-cache-dir -r requirements/testing/requirements.txt -r requirements/merge_bot/requirements.txt -r requirements/app/requirements.txt -r requirements/api/requirements.txt