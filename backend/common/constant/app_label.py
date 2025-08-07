from enum import Enum


class ModelAppLabel(str, Enum):
    SYSTEM = "system"
    ADMIN = "admin"
    DOCTOR = "doctor"
    SECRETARY = "secretary"
    PATIENT = "patient"
    MASTER = "master"
    APPOINTMENT = "appointment"
    COMMON = "common"
    TREATMENT = "treatment"
    PHARMACY = "pharmacy"
    INSURANCE = "insurance"
