FROM --platform="${TARGETPLATFORM:-linux/amd64}" python:3.12.2-slim

RUN apt-get update  \
    && apt-get install -y --no-install-recommends libpq-dev=15.10-0+deb12u1 gcc=4:12.2.0-3  \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements/api/requirements.txt ./

RUN pip3 install --no-cache-dir -r requirements.txt

COPY src ./src

ENTRYPOINT ["/bin/sh"]

# ENTRYPOINT ["python", "-m", "src.api"]