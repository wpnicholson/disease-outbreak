def create_report(client, test_user):
    user_id, test_run_id = test_user

    """Helper function to create a report associated with test user."""
    response = client.post("/api/reports/", params={"created_by": user_id})
    assert response.status_code == 201, response.text
    return response.json()["id"]


def test_create_report(client, test_user):
    report_id = create_report(client, test_user)
    response = client.get(f"/api/reports/{report_id}")
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert data["status"] == "Draft"


def test_list_reports(client, test_user):
    create_report(client, test_user)
    response = client.get("/api/reports/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1  # At least the one we created


def test_get_specific_report(client, test_user):
    report_id = create_report(client, test_user)
    response = client.get(f"/api/reports/{report_id}")
    assert response.status_code == 200
    assert response.json()["id"] == report_id


def test_get_nonexistent_report(client):
    response = client.get("/api/reports/999999")
    assert response.status_code == 404


def test_update_report_status(client, test_user):
    report_id = create_report(client, test_user)
    update_resp = client.put(f"/api/reports/{report_id}", json={"status": "Submitted"})
    assert update_resp.status_code == 200
    assert update_resp.json()["status"] == "Submitted"


def test_update_nonexistent_report(client):
    response = client.put("/api/reports/999999", json={"status": "Submitted"})
    assert response.status_code == 404


def test_update_non_draft_report(client, test_user):
    report_id = create_report(client, test_user)
    # First, submit the report
    client.put(f"/api/reports/{report_id}", json={"status": "Submitted"})
    # Then, try to update it again
    response = client.put(f"/api/reports/{report_id}", json={"status": "Draft"})
    assert response.status_code == 400


def test_delete_report(client, test_user):
    report_id = create_report(client, test_user)
    delete_resp = client.delete(f"/api/reports/{report_id}")
    assert delete_resp.status_code == 204

    # Ensure report is actually deleted
    get_resp = client.get(f"/api/reports/{report_id}")
    assert get_resp.status_code == 404


def test_delete_nonexistent_report(client):
    response = client.delete("/api/reports/999999")
    assert response.status_code == 404


def test_delete_non_draft_report(client, test_user):
    report_id = create_report(client, test_user)
    client.put(f"/api/reports/{report_id}", json={"status": "Submitted"})
    response = client.delete(f"/api/reports/{report_id}")
    assert response.status_code == 400


def test_submit_report_without_required_links(client, test_user):
    report_id = create_report(client, test_user)
    response = client.post(f"/api/reports/{report_id}/submit")
    assert response.status_code == 400


def test_submit_nonexistent_report(client):
    response = client.post("/api/reports/999999/submit")
    assert response.status_code == 404


def test_submit_non_draft_report(client, test_user):
    report_id = create_report(client, test_user)
    client.put(f"/api/reports/{report_id}", json={"status": "Submitted"})
    response = client.post(f"/api/reports/{report_id}/submit")
    assert response.status_code == 400


def test_get_recent_reports(client):
    response = client.get("/api/reports/recent")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
