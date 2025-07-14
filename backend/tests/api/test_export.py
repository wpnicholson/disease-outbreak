from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)


def test_export_formats():
    json_resp = client.get("/api/reports/export/json")
    assert json_resp.status_code == 200
    assert isinstance(json_resp.json(), list)

    csv_resp = client.get("/api/reports/export/csv")
    assert csv_resp.status_code == 200
    assert "text/csv" in csv_resp.headers["content-type"]
