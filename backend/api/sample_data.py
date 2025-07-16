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
import uuid


def create_sample_data(db: Session, created_by_user_id: int):
    """
    Creates sample reporters, patients, reports, and diseases.
    - 5 reporters.
    - 15 patients.
    - 15 reports (5 draft, 5 submitted, 5 approved), each linked to one reporter, one disease, and 1-3 patients.
    """
    unique_str = str(uuid.uuid4())[:8]
    today = date.today()

    # ---------------------------
    # Create 5 Reporters
    # ---------------------------
    reporters = []
    for i in range(5):
        reporter = models.Reporter(
            first_name=f"Reporter{i+1}",
            last_name="Smith",
            email=f"reporter{i+1}-{unique_str}@example.com",
            job_title="Epidemiologist",
            phone_number=f"+4477009000{i+1}",
            hospital_name=f"Hospital {i+1}",
            hospital_address=f"{i+1} Main Street, City",
        )
        reporters.append(reporter)
    db.add_all(reporters)
    db.commit()
    [db.refresh(r) for r in reporters]

    # ---------------------------
    # Create 15 Patients
    # ---------------------------
    patients = []
    for i in range(15):
        patient = models.Patient(
            first_name=f"Patient{i+1}",
            last_name="Lastname",
            date_of_birth=today - timedelta(days=(20 + i) * 365),
            gender=GenderEnum.male if i % 2 == 0 else GenderEnum.female,
            medical_record_number=f"MRN-{unique_str}-{i+1}",
            patient_address=f"{i+1} Health St, City",
            emergency_contact=f"Emergency Contact {i+1}",
        )
        patients.append(patient)
    db.add_all(patients)
    db.commit()
    [db.refresh(p) for p in patients]

    # ---------------------------
    # Create 15 Reports (5 draft, 5 submitted, 5 approved)
    # Each report has:
    #   - Reporter
    #   - Disease (1:1)
    #   - 1-3 Patients (many-to-many)
    # ---------------------------
    report_states = (
        [ReportStateEnum.draft] * 5
        + [ReportStateEnum.submitted] * 5
        + [ReportStateEnum.approved] * 5
    )

    disease_names = ["Influenza", "Ebola", "COVID-19", "Malaria", "Cholera"]
    severity_levels = [
        SeverityLevelEnum.low,
        SeverityLevelEnum.medium,
        SeverityLevelEnum.high,
        SeverityLevelEnum.critical,
    ]
    disease_categories = [
        DiseaseCategoryEnum.viral,
        DiseaseCategoryEnum.bacterial,
        DiseaseCategoryEnum.parasitic,
        DiseaseCategoryEnum.other,
    ]

    reports = []
    for idx, status in enumerate(report_states):
        report = models.Report(
            status=status,
            created_by=created_by_user_id,
            reporter=reporters[idx % 5],
        )
        db.add(report)
        db.commit()
        db.refresh(report)

        # Assign Disease (1-to-1)
        disease = models.Disease(
            disease_name=f"{disease_names[idx % 5]}-{unique_str}-{idx+1}",
            disease_category=disease_categories[idx % len(disease_categories)],
            date_detected=today - timedelta(days=5 + idx),
            symptoms=["fever", "cough"] if idx % 2 == 0 else ["vomiting", "diarrhea"],
            severity_level=severity_levels[idx % len(severity_levels)],
            treatment_status=TreatmentStatusEnum.ongoing,
            report_id=report.id,
        )
        db.add(disease)

        # Link 1-3 Patients
        patient_subset = patients[idx % 15 : (idx % 15) + (idx % 3) + 1]
        report.patients.extend(patient_subset)

        reports.append(report)

    db.commit()

    print(
        "✅ Seeded 5 reporters, 15 patients, 15 reports (draft/submitted/approved), each with a disease and patients."
    )
