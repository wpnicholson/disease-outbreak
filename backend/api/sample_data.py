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


def create_sample_data(db: Session, user_id: int):
    unique_str = str(uuid.uuid4())
    today = date.today()

    # ---------------------------
    # Create 5 Sample Reporters
    # ---------------------------
    phone_numbers = [
        "+447700900001",
        "+447700900002",
        "+447700900003",
        "+447700900004",
        "+447700900005",
        "+447700900006",
    ]
    reporters = [
        models.Reporter(
            first_name=f"Reporter{i}",
            last_name="Smith",
            email=f"reporter{i}-{unique_str}@example.com",
            job_title="Epidemiologist",
            phone_number=phone_numbers[i],
            hospital_name=f"Hospital {i}",
            hospital_address=f"{i} Main Street, City",
        )
        for i in range(1, 6)
    ]
    db.add_all(reporters)
    db.commit()
    for reporter in reporters:
        db.refresh(reporter)

    # ---------------------------
    # Create 15 Reports
    # ---------------------------
    report_states = (
        [ReportStateEnum.draft] * 5
        + [ReportStateEnum.submitted] * 5
        + [ReportStateEnum.approved] * 5
    )

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
    # Create 15 Patients and Diseases (1:1 with Reports)
    # ---------------------------
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

    for idx, report in enumerate(reports):
        # Patient
        patient = models.Patient(
            first_name=f"Patient{idx + 1}",
            last_name="Lastname",
            date_of_birth=today - timedelta(days=(20 + idx) * 365),
            gender=GenderEnum.male if idx % 2 == 0 else GenderEnum.female,
            medical_record_number=f"MRN-{idx + 1}",
            patient_address=f"{idx + 1} Health St, City",
            emergency_contact=f"Emergency Contact {idx + 1}",
            report_id=report.id,
        )
        db.add(patient)

        # Disease
        disease = models.Disease(
            disease_name=disease_names[idx % len(disease_names)],
            disease_category=disease_categories[idx % len(disease_categories)],
            date_detected=today - timedelta(days=5 + idx),
            symptoms=["fever", "cough"] if idx % 2 == 0 else ["vomiting", "diarrhea"],
            severity_level=severity_levels[idx % len(severity_levels)],
            treatment_status=TreatmentStatusEnum.ongoing,
            report_id=report.id,
        )
        db.add(disease)

    db.commit()
