from sqlalchemy.orm import Session
from datetime import date, timedelta
from api import models
from api.enums import (
    GenderEnum,
    DiseaseCategoryEnum,
    SeverityLevelEnum,
    TreatmentStatusEnum,
    ReportStateEnum,
)


def create_sample_data(db: Session, user_id: int):
    # ---------------------------
    # Create Sample Reporters
    # ---------------------------
    reporters = [
        models.Reporter(
            first_name="Alice",
            last_name="Johnson",
            email="alice.johnson@example.com",
            job_title="Infectious Disease Specialist",
            phone_number="+15551230001",
            hospital_name="Central City Hospital",
            hospital_address="123 Main St, Central City",
        ),
        models.Reporter(
            first_name="Bob",
            last_name="Smith",
            email="bob.smith@example.com",
            job_title="Epidemiologist",
            phone_number="+15551230002",
            hospital_name="Westside Clinic",
            hospital_address="456 West Rd, West City",
        ),
        models.Reporter(
            first_name="Carol",
            last_name="Williams",
            email="carol.williams@example.com",
            job_title="Field Researcher",
            phone_number="+15551230003",
            hospital_name="North General Hospital",
            hospital_address="789 North Blvd, North Town",
        ),
    ]
    db.add_all(reporters)
    db.commit()

    # Refresh to get IDs
    for reporter in reporters:
        db.refresh(reporter)

    # ---------------------------
    # Create Reports in Different States
    # ---------------------------
    report_states = [
        ReportStateEnum.draft,
        ReportStateEnum.submitted,
        ReportStateEnum.approved,
    ]
    reports = []
    for idx, state in enumerate(report_states):
        report = models.Report(
            status=state,
            created_by=user_id,
            reporter_id=reporters[idx % len(reporters)].id,
        )
        db.add(report)
        reports.append(report)

    db.commit()

    for report in reports:
        db.refresh(report)

    # ---------------------------
    # Create Patients
    # ---------------------------
    today = date.today()
    patients = []
    for idx in range(10):
        patient = models.Patient(
            first_name=f"Patient{idx}",
            last_name=f"Lastname{idx}",
            date_of_birth=today - timedelta(days=(20 + idx) * 365),
            gender=GenderEnum.male if idx % 2 == 0 else GenderEnum.female,
            medical_record_number=f"MRN-{idx}",
            patient_address=f"{idx} Some Street, City",
            emergency_contact=f"Emergency Contact {idx}",
            report_id=reports[idx % len(reports)].id,
        )
        db.add(patient)
        patients.append(patient)
    db.commit()

    for patient in patients:
        db.refresh(patient)

    # ---------------------------
    # Create Diseases
    # ---------------------------
    disease_names = ["Influenza", "Ebola", "COVID-19", "Malaria", "Cholera"]
    for idx, report in enumerate(reports):
        disease = models.Disease(
            disease_name=disease_names[idx % len(disease_names)],
            disease_category=(
                DiseaseCategoryEnum.viral
                if idx % 2 == 0
                else DiseaseCategoryEnum.bacterial
            ),
            date_detected=today - timedelta(days=5 + idx),
            symptoms=["fever", "cough"] if idx % 2 == 0 else ["vomiting", "diarrhea"],
            severity_level=[
                SeverityLevelEnum.low,
                SeverityLevelEnum.medium,
                SeverityLevelEnum.high,
            ][idx % 3],
            treatment_status=TreatmentStatusEnum.ongoing,
            report_id=report.id,
        )
        db.add(disease)

    db.commit()
