from enum import Enum


class SwaggerTag(str, Enum):
    MASTER = "Master Data"
    AUTH = "Authentication"
    ACCOUNT = "Account"
    DOCTOR = "Doctor"
    PATIENT = "Patient"
    APPOINTMENT = "Appointment"
    APPOINTMENT_TREATMENT = "Appointment treatment"
    APPOINTMENT_MEDICINE = "Appointment medicine"
    APPOINTMENT_PRESCRIPTION = "Appointment presctiprion"
    TREATMENT = "Treatment"
    MEDICINE = "Medicine"
    ALLERGY = "Allergy"
    INSURANCE = "Insurance"
