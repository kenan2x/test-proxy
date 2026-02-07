import json
from pathlib import Path
from app.logger import TelemetryLogger


def test_logger_writes_request(tmp_path):
    """Test logger writes request to JSON file"""
    log_dir = tmp_path / "logs"
    logger = TelemetryLogger(log_dir=str(log_dir))

    logger.log_request(
        method="POST",
        path="/telemetry/v1/metrics",
        headers={"Content-Type": "application/json"},
        body={"test": "data"}
    )

    # Check file was created
    log_files = list(log_dir.glob("*.json"))
    assert len(log_files) == 1

    # Check content
    with open(log_files[0]) as f:
        data = json.load(f)

    assert data["method"] == "POST"
    assert data["path"] == "/telemetry/v1/metrics"
    assert data["body"] == {"test": "data"}
    assert "timestamp" in data
