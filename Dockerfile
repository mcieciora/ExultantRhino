FROM python:3.12.2-alpine

WORKDIR /app

COPY requirements/example_app/requirements.txt /app

RUN pip3 install --no-cache-dir -r requirements.txt

ENTRYPOINT ["sleep", "180"]