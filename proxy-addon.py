"""
mitmproxy addon - Cribl telemetry interceptor
Intercepts requests to cdn.cribl.io and returns mock response
"""
from mitmproxy import http
import json
from datetime import datetime

class CriblTelemetryInterceptor:
    def __init__(self):
        print("[INTERCEPTOR] Cribl Telemetry Interceptor loaded")
        print("[INTERCEPTOR] Intercepting: cdn.cribl.io")

    def request(self, flow: http.HTTPFlow) -> None:
        if "cdn.cribl.io" in flow.request.pretty_host:
            # Parse query parameters
            query_params = dict(flow.request.query) if flow.request.query else {}

            # Print telemetry to stdout
            print("=" * 60)
            print(f"[TELEMETRY] {datetime.utcnow().isoformat()}")
            print(f"[TELEMETRY] {flow.request.method} {flow.request.pretty_url}")
            print(f"[TELEMETRY] Query params: {json.dumps(query_params, indent=2)}")
            print("=" * 60)

            # Create mock response
            flow.response = http.Response.make(
                200,
                b"cribl /// living the stream!\n",
                {"Content-Type": "text/html; charset=utf-8"}
            )

addons = [CriblTelemetryInterceptor()]
