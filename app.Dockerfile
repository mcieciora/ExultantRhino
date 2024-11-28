FROM --platform="${TARGETPLATFORM:-linux/amd64}" python:3.12.2-slim

RUN apt-get update apt-get install -y --no-install-recommends libpq-dev gcc

WORKDIR /app

COPY requirements/app/requirements.txt ./

RUN pip3 install --no-cache-dir -r requirements.txt

COPY src ./src

ENTRYPOINT ["python", "-m", "streamlit", "run", "src/Dashboard.py", "--server.port=8501", "--server.address=0.0.0.0"]