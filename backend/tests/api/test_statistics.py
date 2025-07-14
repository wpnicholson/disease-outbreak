from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)


def test_statistics_returns_zero():
    resp = client.get("/api/statistics")
    assert resp.status_code == 200
    assert resp.json()["total_reports"] >= 0
