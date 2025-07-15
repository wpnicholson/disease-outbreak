def test_patient_validation(client, test_user):
    user_id, test_run_id = test_user

    report_id = client.post("/api/reports/", params={"created_by": user_id}).json()[
        "id"
    ]
    client.post(
        f"/api/reports/{report_id}/reporter",
        json={
            "first_name": "Dr.",
            "last_name": "Who",
            "email": f"doctor-{test_run_id}@example.com",
            "job_title": "Doctor",
            "phone_number": "+111111111",
            "hospital_name": "TARDIS",
            "hospital_address": "Everywhere",
        },
    )

    future_dob = "2999-01-01"
    invalid_resp = client.post(
        f"/api/reports/{report_id}/patient",
        json={
            "first_name": "John",
            "last_name": "Doe",
            "date_of_birth": future_dob,
            "gender": "Male",
            "medical_record_number": f"ABC123-{test_run_id}",
            "patient_address": "123 St",
            "emergency_contact": "None",
        },
    )
    assert invalid_resp.status_code == 400


def test_patient_missing_reporter(client, test_user):
    user_id, test_run_id = test_user

    report_id = client.post("/api/reports/", params={"created_by": user_id}).json()[
        "id"
    ]
    response = client.post(
        f"/api/reports/{report_id}/patient",
        json={
            "first_name": "Anna",
            "last_name": "Smith",
            "date_of_birth": "1990-01-01",
            "gender": "Female",
            "medical_record_number": f"MRN001-{test_run_id}",
            "patient_address": "Address",
            "emergency_contact": "N/A",
        },
    )
    assert response.status_code == 400


def test_get_patient_not_found(client, test_user):
    invalid_report = 99999
    response = client.get(f"/api/reports/{invalid_report}/patient")
    assert response.status_code == 404


def test_add_patient_success(client, test_user):
    user_id, test_run_id = test_user

    report_id = client.post("/api/reports/", params={"created_by": user_id}).json()[
        "id"
    ]
    client.post(
        f"/api/reports/{report_id}/reporter",
        json={
            "first_name": "Dr.",
            "last_name": "Who",
            "email": f"doctor-{test_run_id}@example.com",
            "job_title": "Doctor",
            "phone_number": "+14155552671",
            "hospital_name": "TARDIS",
            "hospital_address": "Everywhere",
        },
    )
    response = client.post(
        f"/api/reports/{report_id}/patient",
        json={
            "first_name": "Amy",
            "last_name": "Pond",
            "date_of_birth": "1990-01-01",
            "gender": "Female",
            "medical_record_number": f"MRN100-{test_run_id}",
            "patient_address": "Leadworth",
            "emergency_contact": "Rory",
        },
    )
    assert response.status_code == 201


def test_patient_duplicate_mrn_reuse(client, test_user):
    user_id, test_run_id = test_user

    report1 = client.post("/api/reports/", params={"created_by": user_id}).json()["id"]
    report2 = client.post("/api/reports/", params={"created_by": user_id}).json()["id"]
    client.post(
        f"/api/reports/{report1}/reporter",
        json={
            "first_name": "Doc",
            "last_name": "One",
            "email": f"doc1-{test_run_id}@example.com",
            "job_title": "Doctor",
            "phone_number": "+14155552671",
            "hospital_name": "Metro",
            "hospital_address": "Addr",
        },
    )
    client.post(
        f"/api/reports/{report2}/reporter",
        json={
            "first_name": "Doc",
            "last_name": "Two",
            "email": f"doc2-{test_run_id}@example.com",
            "job_title": "Doctor",
            "phone_number": "+14155552672",
            "hospital_name": "Metro",
            "hospital_address": "Addr",
        },
    )
    patient_payload = {
        "first_name": "Sam",
        "last_name": "Smith",
        "date_of_birth": "1980-01-01",
        "gender": "Male",
        "medical_record_number": f"DUPLICATE123-{test_run_id}",
        "patient_address": "Place",
        "emergency_contact": "N/A",
    }
    client.post(f"/api/reports/{report1}/patient", json=patient_payload)
    response = client.post(f"/api/reports/{report2}/patient", json=patient_payload)
    assert response.status_code == 201


def test_edit_patient_after_submission_forbidden(client, test_user):
    user_id, test_run_id = test_user

    report_id = client.post("/api/reports/", params={"created_by": user_id}).json()[
        "id"
    ]
    response = client.post(
        f"/api/reports/{report_id}/reporter",
        json={
            "first_name": "X",
            "last_name": "Y",
            "email": f"xy-{test_run_id}@example.com",
            "job_title": "Doctor",
            "phone_number": "+15555555555",
            "hospital_name": "ABC",
            "hospital_address": "Addr",
        },
    )
    assert response.status_code == 201

    response = client.post(
        f"/api/reports/{report_id}/patient",
        json={
            "first_name": "Pat",
            "last_name": "Ent",
            "date_of_birth": "1970-01-01",
            "gender": "Male",
            "medical_record_number": f"LOCKED123-{test_run_id}",
            "patient_address": "Somewhere",
            "emergency_contact": "No one",
        },
    )
    assert response.status_code == 201

    response = client.post(
        f"/api/reports/{report_id}/disease",
        json={
            "disease_name": "Cold",
            "disease_category": "Viral",
            "date_detected": "2020-01-01",
            "symptoms": ["Sneezing"],
            "severity_level": "Low",
            "treatment_status": "Ongoing",
        },
    )
    assert response.status_code == 200

    response = client.post(f"/api/reports/{report_id}/submit")
    assert response.status_code == 200

    submitted_report = client.get(f"/api/reports/{report_id}").json()
    print(f"Submitted report status: {submitted_report['status']}")

    response = client.post(
        f"/api/reports/{report_id}/patient",
        json={
            "first_name": "Patch",
            "last_name": "Edit",
            "date_of_birth": "1970-01-01",
            "gender": "Male",
            "medical_record_number": f"LOCKED123-{test_run_id}",
            "patient_address": "New Addr",
            "emergency_contact": "Still no one",
        },
    )
    assert response.status_code == 400
