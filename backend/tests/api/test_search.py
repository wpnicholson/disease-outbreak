from fastapi.testclient import TestClient
from api.main import app
from api.enums import ReportStateEnum

client = TestClient(app)


def test_search_reports_empty():
    params = {"status": ReportStateEnum.submitted.value}

    resp = client.get("/api/reports/search", params=params)
    print(resp.json())
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)
