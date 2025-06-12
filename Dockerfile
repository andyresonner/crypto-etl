# — Dockerfile —
FROM python:3.12-slim

# install deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# copy code
COPY . /app
WORKDIR /app

# default command: run the ETL
CMD ["python", "-m", "crypto_etl.main"]
