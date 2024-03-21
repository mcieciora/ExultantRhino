FROM python:3.12.2-slim

RUN apt-get update && apt-get install -y --no-install-recommends libpq-dev=15.6-0+deb12u1 gcc=4:12.2.0-3 && apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements/app/requirements.txt ./
COPY src ./src

RUN pip3 install --no-cache-dir -r requirements.txt

ENTRYPOINT ["python", "-m", "streamlit", "run", "src/dashboard.py", "--server.port=8501", "--server.address=0.0.0.0"]