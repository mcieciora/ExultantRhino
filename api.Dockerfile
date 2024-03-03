FROM python:3.12.2-slim

RUN apt update
RUN apt install libpq-dev gcc -y

WORKDIR /app

COPY requirements/api/requirements.txt ./
COPY src ./src

RUN pip3 install --no-cache-dir -r requirements.txt

ENTRYPOINT ["python", "-m", "src.api"]