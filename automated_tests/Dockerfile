FROM python:3.13.1-slim

RUN apt update && apt install -y libpq-dev firefox-esr

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