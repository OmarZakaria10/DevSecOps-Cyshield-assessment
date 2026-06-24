"""
Tests for the /health endpoint.
"""


def test_health_returns_ok(client):
    """Health check must return 200 and a JSON body with status 'ok'."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.get_json() == {"status": "ok"}
