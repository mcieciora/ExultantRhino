FROM python:3.11-slim
MAINTAINER mcieciora

COPY requirements.txt /app

WORKDIR /app

RUN pip3 install -r requirements.txt

ENTRYPOINT ["python3"]