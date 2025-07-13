import enum


class GenderEnum(str, enum.Enum):
    male = "Male"
    female = "Female"
    other = "Other"


# Disease category (required, enum: Bacterial/Viral/Parasitic/Other).
class DiseaseCategoryEnum(str, enum.Enum):
    bacterial = "Bacterial"
    viral = "Viral"
    parasitic = "Parasitic"
    other = "Other"


# Severity level (required, enum: Low/Medium/High/Critical).
class SeverityLevelEnum(str, enum.Enum):
    low = "Low"
    medium = "Medium"
    high = "High"
    critical = "Critical"


# Treatment status (required, enum: None/Ongoing/Completed).
class TreatmentStatusEnum(str, enum.Enum):
    none = "None"
    ongoing = "Ongoing"
    completed = "Completed"


# Report states:
# - Draft - editable, incomplete reports.
# - Submitted - complete, read-only reports.
# - Under Review - being reviewed by editor (optional feature).
# - Approved - final approved reports.
class ReportStateEnum(str, enum.Enum):
    draft = "Draft"
    submitted = "Submitted"
    under_review = "Under Review"
    approved = "Approved"
