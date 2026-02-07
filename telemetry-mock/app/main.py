import time
from fastapi import FastAPI, Request
from fastapi.responses import Response
from app.logger import TelemetryLogger

app = FastAPI(title="Cribl Telemetry Mock Server", version="1.0.0")

# Initialize logger at module level
logger = TelemetryLogger(log_dir="logs")


@app.get("/health")
async def health():
    """Health check endpoint"""
    return {"status": "healthy"}


@app.get("/telemetry/index.html")
async def telemetry_endpoint(request: Request):
    """
    Real Cribl telemetry endpoint.
    Based on Task 4 analysis - Cribl uses GET /telemetry/index.html, not POST /telemetry/v1/metrics.
    Returns simple HTML text matching actual Cribl response.
    """
    start_time = time.perf_counter()

    # Extract all query parameters
    query_params = dict(request.query_params)

    # Log request
    log_file = logger.log_request(
        method="GET",
        path="/telemetry/index.html",
        headers=dict(request.headers),
        body=None,
        query_params=query_params,
    )

    # Return simple HTML response matching real Cribl behavior
    response_body = "cribl /// living the stream!\n"

    # Calculate latency
    latency_ms = (time.perf_counter() - start_time) * 1000

    # Log response
    logger.log_response(log_file, 200, response_body, latency_ms)

    return Response(content=response_body, media_type="text/html")
