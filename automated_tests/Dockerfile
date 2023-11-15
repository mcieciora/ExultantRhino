FROM python:3.11-slim

COPY requirements.txt requirements/requirements-testing.txt pytest.ini app/

COPY automated_tests app/automated_tests/

COPY src app/src/

WORKDIR app

RUN python3 -m pip install -r requirements.txt
RUN python3 -m pip install -r requirements-testing.txt