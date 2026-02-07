# Dockerfile for Cribl Telemetry Mock Server

FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ ./app/

# Copy pre-generated certificate with SAN
COPY telemetry-cert.pem /app/cert.pem
COPY telemetry-key.pem /app/key.pem

EXPOSE 8000 80 443

# Run on both HTTP (80) and HTTPS (443) simultaneously
CMD uvicorn app.main:app --host 0.0.0.0 --port 80 & \
    uvicorn app.main:app --host 0.0.0.0 --port 443 --ssl-keyfile /app/key.pem --ssl-certfile /app/cert.pem
