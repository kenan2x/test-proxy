"""
End-to-end integration tests for the telemetry mock server.

These tests verify that the mock server responds correctly to HTTP requests
and serves telemetry data as expected.
"""
import requests
import time
import pytest


def test_mock_server_responds():
    """Verify the mock server health endpoint responds."""
    response = requests.get("http://localhost:8000/health")
    assert response.status_code == 200


def test_telemetry_endpoint_works():
    """Verify telemetry endpoint serves content with Cribl tracking."""
    response = requests.get("http://localhost:8000/telemetry/index.html?v=test")
    assert response.status_code == 200
    assert "cribl" in response.text.lower()


def test_telemetry_script_served():
    """Verify telemetry JavaScript is served correctly."""
    response = requests.get("http://localhost:8000/telemetry/cribl.js")
    assert response.status_code == 200
    assert "function" in response.text or "var" in response.text


def test_telemetry_with_query_params():
    """Verify telemetry endpoints handle query parameters."""
    response = requests.get("http://localhost:8000/telemetry/index.html?version=1.2.3&env=prod")
    assert response.status_code == 200
    assert response.headers.get("content-type") in ["text/html", "text/html; charset=utf-8"]


def test_metrics_endpoint():
    """Verify metrics endpoint is accessible."""
    response = requests.get("http://localhost:8000/metrics")
    assert response.status_code == 200
