FROM python:3.12.2-slim

RUN apt-get update && install libpq-dev gcc -y && apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY pytest.ini ./

WORKDIR /app/requirements
COPY requirements/ .

WORKDIR /app/automated_tests
COPY automated_tests .

WORKDIR /app/src
COPY src .

WORKDIR /app
RUN python -m pip install --no-cache-dir -r requirements/app/requirements.txt -r requirements/api/requirements.txt -r requirements/testing/requirements.txt