import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional


class TelemetryLogger:
    """Logger for telemetry requests and responses"""

    def __init__(self, log_dir: str = "logs"):
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(exist_ok=True, parents=True)

    def log_request(
        self,
        method: str,
        path: str,
        headers: Dict[str, str],
        body: Optional[Any] = None,
        query_params: Optional[Dict[str, str]] = None,
    ) -> str:
        """Log incoming request and return log file path"""
        timestamp = datetime.utcnow()
        log_data = {
            "timestamp": timestamp.isoformat(),
            "type": "request",
            "method": method,
            "path": path,
            "headers": headers,
            "query_params": query_params or {},
            "body": body,
        }

        filename = f"telemetry_{timestamp.strftime('%Y%m%d_%H%M%S_%f')}.json"
        log_file = self.log_dir / filename

        with open(log_file, "w") as f:
            json.dump(log_data, f, indent=2)

        print(f"[LOG] {method} {path} -> {log_file}")
        return str(log_file)

    def log_response(
        self,
        log_file: str,
        status_code: int,
        body: Any,
        latency_ms: float,
    ):
        """Append response data to existing log file"""
        log_path = Path(log_file)

        with open(log_path) as f:
            log_data = json.load(f)

        log_data["response"] = {
            "status_code": status_code,
            "body": body,
            "latency_ms": latency_ms,
        }

        with open(log_path, "w") as f:
            json.dump(log_data, f, indent=2)

        print(f"[LOG] Response {status_code} - {latency_ms:.2f}ms")
