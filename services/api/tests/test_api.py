from fastapi.testclient import TestClient

from dumpingdesk_api.main import app


def test_health_endpoint_reports_ready():
    client = TestClient(app)

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok", "service": "dumpingdesk-api"}
