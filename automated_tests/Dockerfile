FROM python:3.12.2-alpine

WORKDIR /app
COPY requirements/testing/requirements.txt ./requirements-testing.txt
COPY requirements/example_app/requirements.txt pytest.ini ./

WORKDIR /app/automated_tests
COPY automated_tests .

WORKDIR /app/src
COPY src .

WORKDIR /app/tools/python
COPY tools/python .

WORKDIR /app
RUN python -m pip install --no-cache-dir -r requirements.txt -r requirements-testing.txt