FROM python:3.10.4-alpine3.15

MAINTAINER mcieciora

COPY ./src /app

COPY requirements.txt /app

WORKDIR /app

RUN pip install -r requirements.txt

CMD [ "python3", "main.py" ]