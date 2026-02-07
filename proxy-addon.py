"""
mitmproxy addon - Cribl telemetry interceptor
Intercepts requests to cdn.cribl.io and returns mock response
"""
from mitmproxy import http
import json
from datetime import datetime
import os

LOG_DIR = "/logs"

class CriblTelemetryInterceptor:
    def __init__(self):
        os.makedirs(LOG_DIR, exist_ok=True)
        print("[INTERCEPTOR] Cribl Telemetry Interceptor loaded")
        print("[INTERCEPTOR] Intercepting: cdn.cribl.io")

    def request(self, flow: http.HTTPFlow) -> None:
        # Check if this is a request to cdn.cribl.io
        if "cdn.cribl.io" in flow.request.pretty_host:
            print(f"[INTERCEPTOR] Caught: {flow.request.method} {flow.request.pretty_url}")

            # Log the request
            self._log_request(flow)

            # Create mock response
            flow.response = http.Response.make(
                200,
                b"cribl /// living the stream!\n",
                {
                    "Content-Type": "text/html; charset=utf-8",
                    "Server": "cribl-mock",
                    "X-Intercepted": "true"
                }
            )
            print(f"[INTERCEPTOR] Responded with mock response")

    def _log_request(self, flow: http.HTTPFlow):
        """Log request to JSON file"""
        timestamp = datetime.utcnow()

        # Parse query parameters
        query_params = {}
        if flow.request.query:
            query_params = dict(flow.request.query)

        log_data = {
            "timestamp": timestamp.isoformat(),
            "method": flow.request.method,
            "url": flow.request.pretty_url,
            "path": flow.request.path,
            "host": flow.request.pretty_host,
            "headers": dict(flow.request.headers),
            "query_params": query_params,
        }

        # Write to file
        filename = f"telemetry_{timestamp.strftime('%Y%m%d_%H%M%S_%f')}.json"
        filepath = os.path.join(LOG_DIR, filename)

        try:
            with open(filepath, 'w') as f:
                json.dump(log_data, f, indent=2)
            print(f"[INTERCEPTOR] Logged to: {filename}")
        except Exception as e:
            print(f"[INTERCEPTOR] Log error: {e}")

addons = [CriblTelemetryInterceptor()]
