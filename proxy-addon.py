"""
mitmproxy addon - Cribl telemetry interceptor
Intercepts requests to cdn.cribl.io and returns mock response
"""
from mitmproxy import http
import json
import sys
from datetime import datetime

class CriblTelemetryInterceptor:
    def __init__(self):
        print("[INTERCEPTOR] Cribl Telemetry Interceptor loaded", flush=True)
        print("[INTERCEPTOR] Intercepting: cdn.cribl.io", flush=True)

    def request(self, flow: http.HTTPFlow) -> None:
        if "cdn.cribl.io" in flow.request.pretty_host:
            # Parse query parameters
            query_params = dict(flow.request.query) if flow.request.query else {}

            # Print telemetry to stdout
            print("=" * 60, flush=True)
            print(f"[TELEMETRY] {datetime.utcnow().isoformat()}", flush=True)
            print(f"[TELEMETRY] {flow.request.method} {flow.request.pretty_url}", flush=True)
            print(f"[TELEMETRY] Query params: {json.dumps(query_params, indent=2)}", flush=True)
            print("=" * 60, flush=True)

            # Create mock response
            flow.response = http.Response.make(
                200,
                b"cribl /// living the stream!\n",
                {"Content-Type": "text/html; charset=utf-8"}
            )

addons = [CriblTelemetryInterceptor()]
