import enum


class GenderEnum(str, enum.Enum):
    male = "Male"
    female = "Female"
    other = "Other"


class DiseaseCategoryEnum(str, enum.Enum):
    bacterial = "Bacterial"
    viral = "Viral"
    parasitic = "Parasitic"
    other = "Other"


class SeverityLevelEnum(str, enum.Enum):
    low = "Low"
    medium = "Medium"
    high = "High"
    critical = "Critical"


class TreatmentStatusEnum(str, enum.Enum):
    none = "None"
    ongoing = "Ongoing"
    completed = "Completed"


class ReportStateEnum(str, enum.Enum):
    draft = "Draft"
    submitted = "Submitted"
    under_review = "Under Review"
    approved = "Approved"
