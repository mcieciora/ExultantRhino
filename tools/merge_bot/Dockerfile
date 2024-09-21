FROM python:3.12.2-alpine

WORKDIR /app

COPY requirements/merge_bot/requirements.txt /app
COPY tools/merge_bot/merge_bot.py .

RUN pip3 install --no-cache-dir -r requirements.txt

ENTRYPOINT ["python", "merge_bot.py"]