import pytest
from fastapi.testclient import TestClient
from app.main import app


client = TestClient(app)


def test_health_endpoint():
    """Test that health endpoint returns 200 OK"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_telemetry_endpoint_get():
    """Test GET /telemetry/index.html endpoint"""
    # Test with query parameters matching real Cribl telemetry
    response = client.get("/telemetry/index.html?v=4.16.1&guid=test-guid&env=prod")

    assert response.status_code == 200
    assert response.headers["content-type"] == "text/html; charset=utf-8"
    assert "cribl" in response.text
    assert "living the stream" in response.text


def test_telemetry_endpoint_no_params():
    """Test telemetry endpoint works without query parameters"""
    response = client.get("/telemetry/index.html")

    assert response.status_code == 200
    assert "cribl" in response.text
