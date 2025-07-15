def test_reporter_flow(client, test_user):
    user_id, test_run_id = test_user
    report_resp = client.post("/api/reports/", params={"created_by": user_id})
    report_id = report_resp.json()["id"]

    reporter_resp = client.post(
        f"/api/reports/{report_id}/reporter",
        json={
            "first_name": "Alice",
            "last_name": "Smith",
            "email": f"alice-{test_run_id}@example.com",
            "job_title": "Physician",
            "phone_number": "+14155552671",
            "hospital_name": "City Hospital",
            "hospital_address": "123 Main St",
        },
    )
    assert reporter_resp.status_code == 201

    get_resp = client.get(f"/api/reports/{report_id}/reporter")
    assert get_resp.status_code == 200
    assert get_resp.json()["email"] == f"alice-{test_run_id}@example.com"
