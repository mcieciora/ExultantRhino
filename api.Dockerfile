FROM python:3.13.1-slim

RUN apt update && apt install -y libpq-dev

WORKDIR /app

COPY requirements/api/requirements.txt ./

RUN pip3 install --no-cache-dir -r requirements.txt

COPY src ./src

ENTRYPOINT ["python", "-m", "src.api"]