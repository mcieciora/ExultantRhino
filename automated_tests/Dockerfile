FROM python:3.12.2-slim

RUN apt update
RUN apt install libpq-dev gcc -y

WORKDIR /app
COPY pytest.ini ./
COPY .env_test ./
COPY requirements/api/requirements.txt ./requirements-api.txt
COPY requirements/app/requirements.txt ./requirements-app.txt
COPY requirements/testing/requirements.txt ./requirements-testing.txt

WORKDIR /app/automated_tests
COPY automated_tests .

WORKDIR /app/src
COPY src .

WORKDIR /app
RUN python -m pip install --no-cache-dir -r requirements-app.txt -r requirements-api.txt -r requirements-testing.txt