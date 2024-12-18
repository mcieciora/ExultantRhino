FROM python:3.13.1-slim

WORKDIR /app

COPY requirements/api/requirements.txt ./

RUN pip3 install --no-cache-dir -r requirements.txt

COPY src ./src

ENTRYPOINT ["python", "-m", "src.api"]