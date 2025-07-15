from api.enums import ReportStateEnum


def test_search_reports_empty(client):
    params = {"status": ReportStateEnum.submitted.value}

    resp = client.get("/api/reports/search", params=params)
    print(resp.json())
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)
