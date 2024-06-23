FROM python:3.12.2-slim

RUN echo "deb http://deb.debian.org/debian/ unstable main contrib non-free" >> /etc/apt/sources.list.d/debian.list
RUN apt-get update

RUN apt-get install -y libpq-dev gcc firefox

WORKDIR /app
COPY pytest.ini ./

WORKDIR /app/requirements
COPY requirements/ .

WORKDIR /app/automated_tests
COPY automated_tests .

WORKDIR /app/src
COPY src .

WORKDIR /app/tools/python
COPY tools/python .

WORKDIR /app

RUN python -m pip install --no-cache-dir -r requirements/app/requirements.txt -r requirements/api/requirements.txt -r requirements/testing/requirements.txt
