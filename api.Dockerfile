FROM python:3.12.2-slim

RUN apt-get update && install libpq-dev gcc -y && apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements/api/requirements.txt ./
COPY src ./src

RUN pip3 install --no-cache-dir -r requirements.txt

ENTRYPOINT ["python", "-m", "src.api"]