FROM python:3.12.2-slim

RUN apt-get update && install libpq-dev gcc -y && apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements/example_app/requirements.txt /app
COPY requirements/app/requirements.txt ./
COPY src ./src

RUN pip3 install --no-cache-dir -r requirements.txt

ENTRYPOINT ["python", "-m", "streamlit", "run", "src/dashboard.py", "--server.port=8501", "--server.address=0.0.0.0"]