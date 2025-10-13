import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    """Test /health endpoint returns 200."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy", "version": "0.1.0"}

def test_readiness_check():
    """Test /readiness endpoint returns 200."""
    response = client.get("/readiness")
    assert response.status_code == 200
    assert response.json() == {"status": "ready"}

def test_metrics_endpoint():
    """Test /metrics endpoint is accessible."""
    response = client.get("/metrics")
    assert response.status_code == 200
    # Check if it contains Prometheus format (basic check)
    assert "HELP" in response.text or "TYPE" in response.text
