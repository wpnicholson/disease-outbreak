from api.enums import DiseaseCategoryEnum, SeverityLevelEnum, TreatmentStatusEnum


def test_disease_crossfield_validation(client, test_user):
    user_id, test_run_id = test_user

    report_id = client.post("/api/reports/", params={"created_by": user_id}).json()[
        "id"
    ]

    client.post(
        f"/api/reports/{report_id}/reporter",
        json={
            "first_name": "Sam",
            "last_name": "Dean",
            "email": f"sam-{test_run_id}@example.com",
            "job_title": "Doctor",
            "phone_number": "+123123123",
            "hospital_name": "Metro",
            "hospital_address": "456 St",
        },
    )

    client.post(
        f"/api/reports/{report_id}/patient",
        json={
            "first_name": "Jane",
            "last_name": "Doe",
            "date_of_birth": "2000-01-01",
            "gender": "Female",
            "medical_record_number": f"MED-{test_run_id}",
            "patient_address": "789 St",
            "emergency_contact": "N/A",
        },
    )

    response = client.post(
        f"/api/reports/{report_id}/disease",
        json={
            "disease_name": f"Flu-{test_run_id}",
            "disease_category": DiseaseCategoryEnum.viral.value,
            "date_detected": "1999-01-01",
            "symptoms": ["Cough", "Fever"],
            "severity_level": SeverityLevelEnum.low.value,
            "treatment_status": TreatmentStatusEnum.ongoing.value,
        },
    )
    assert response.status_code == 400


def test_get_disease_not_found(client):
    invalid_report = 99999
    response = client.get(f"/api/reports/{invalid_report}/disease")
    assert response.status_code == 404


def test_disease_categories(client):
    response = client.get("/api/reports/diseases/categories")
    assert response.status_code == 200
    assert DiseaseCategoryEnum.viral.value.capitalize() in response.json()


def test_disease_missing_patient(client, test_user):
    user_id, test_run_id = test_user

    report_id = client.post("/api/reports/", params={"created_by": user_id}).json()[
        "id"
    ]

    client.post(
        f"/api/reports/{report_id}/reporter",
        json={
            "first_name": "Mark",
            "last_name": "Jones",
            "email": f"mark-{test_run_id}@example.com",
            "job_title": "Doctor",
            "phone_number": "+222222222",
            "hospital_name": "Metro",
            "hospital_address": "456 St",
        },
    )

    response = client.post(
        f"/api/reports/{report_id}/disease",
        json={
            "disease_name": f"Cold-{test_run_id}",
            "disease_category": DiseaseCategoryEnum.viral.value,
            "date_detected": "2020-01-01",
            "symptoms": ["Sneezing"],
            "severity_level": SeverityLevelEnum.low.value,
            "treatment_status": TreatmentStatusEnum.ongoing.value,
        },
    )
    assert response.status_code == 400


def test_disease_add_and_overwrite_success(client, test_user):
    user_id, test_run_id = test_user

    report_id = client.post("/api/reports/", params={"created_by": user_id}).json()[
        "id"
    ]

    client.post(
        f"/api/reports/{report_id}/reporter",
        json={
            "first_name": "Jane",
            "last_name": "Doe",
            "email": f"jane-{test_run_id}@example.com",
            "job_title": "Doctor",
            "phone_number": "+14155552671",
            "hospital_name": "Gen Hospital",
            "hospital_address": "Addr",
        },
    )

    client.post(
        f"/api/reports/{report_id}/patient",
        json={
            "first_name": "John",
            "last_name": "Doe",
            "date_of_birth": "1990-01-01",
            "gender": "Male",
            "medical_record_number": f"PAT-{test_run_id}",
            "patient_address": "Addr",
            "emergency_contact": "None",
        },
    )

    first_response = client.post(
        f"/api/reports/{report_id}/disease",
        json={
            "disease_name": f"Covid-{test_run_id}",
            "disease_category": DiseaseCategoryEnum.viral.value,
            "date_detected": "2021-01-01",
            "symptoms": ["Cough"],
            "severity_level": SeverityLevelEnum.high.value,
            "treatment_status": TreatmentStatusEnum.ongoing.value,
        },
    )
    assert first_response.status_code == 200

    overwrite_response = client.post(
        f"/api/reports/{report_id}/disease",
        json={
            "disease_name": f"Influenza-{test_run_id}",
            "disease_category": DiseaseCategoryEnum.viral.value,
            "date_detected": "2021-01-01",
            "symptoms": ["Fever"],
            "severity_level": SeverityLevelEnum.medium.value,
            "treatment_status": TreatmentStatusEnum.ongoing.value,
        },
    )
    assert overwrite_response.status_code == 200


def test_edit_disease_after_submission_forbidden(client, test_user):
    user_id, test_run_id = test_user

    report_id = client.post("/api/reports/", params={"created_by": user_id}).json()[
        "id"
    ]

    client.post(
        f"/api/reports/{report_id}/reporter",
        json={
            "first_name": "No",
            "last_name": "Edit",
            "email": f"lock{test_run_id}@example.com",
            "job_title": "Doctor",
            "phone_number": "+16665553333",
            "hospital_name": "Metro",
            "hospital_address": "Addr",
        },
    )

    client.post(
        f"/api/reports/{report_id}/patient",
        json={
            "first_name": "Locked",
            "last_name": "Patient",
            "date_of_birth": "1980-01-01",
            "gender": "Male",
            "medical_record_number": f"LOCK-{test_run_id}",
            "patient_address": "Addr",
            "emergency_contact": "None",
        },
    )

    client.post(
        f"/api/reports/{report_id}/disease",
        json={
            "disease_name": f"Typhoid-{test_run_id}",
            "disease_category": DiseaseCategoryEnum.bacterial.value,
            "date_detected": "2019-01-01",
            "symptoms": ["Fever"],
            "severity_level": SeverityLevelEnum.high.value,
            "treatment_status": TreatmentStatusEnum.ongoing.value,
        },
    )

    client.post(f"/api/reports/{report_id}/submit")

    response = client.post(
        f"/api/reports/{report_id}/disease",
        json={
            "disease_name": f"Update-{test_run_id}",
            "disease_category": DiseaseCategoryEnum.other.value,
            "date_detected": "2020-01-01",
            "symptoms": ["N/A"],
            "severity_level": SeverityLevelEnum.critical.value,
            "treatment_status": TreatmentStatusEnum.completed.value,
        },
    )
    assert response.status_code == 400
