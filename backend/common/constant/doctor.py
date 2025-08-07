from enum import unique
from .base import AzooBaseEnum


@unique
class DoctorSettingAleryKey(str, AzooBaseEnum):
    MEDICINE_THRESHOLD: str = "medicine_threshold"
    MEDICINE_EXPIRES_DATE: str = "medicine_expire_date"
    APPOITMENT_ALERT: str = "appointment_alert"
