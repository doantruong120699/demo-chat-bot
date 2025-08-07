from enum import Enum


class DBTable(str, Enum):
    # Admin
    ADMIN = "admin"

    DOCTOR = "doctor"
    SECRETARY = "secretary"
    DOCTOR_SETTING_ALERT = "doctor_setting_alert"
    PATIENT = "patient"
    PATIENT_DETAIL = "patient_detail"
    PATIENT_HISTORY = "patient_history"
    PATIENT_RISK = "patient_risk"
    PATIENT_UPLOAD_FILE = "patient_upload_file"
    APPOINTMENT = "appointment"
    TIME_APPOINTMENT = "time_appointment"
    TREATMENT = "treatment"
    APPOINTMENT_TREATMENT = "appointment_treatment"
    MEDICINE = "medicine"
    MEDICINE_CATEGORY = "medicine_category"
    APPOINTMENT_MEDICINE = "appointment_medicine"
    APPOINTMENT_PRESCRIPTION = "appointment_prescription"
    SYMPTOM = "symptom"
    ALLERGY = "allergy"
    RESPIRATORY_SYMPTOM = "respiratory_symptom"
    DIGESTIVE_SYMPTOM = "digestive_symptom"
    SKIN_SYMPTOM = "skin_symptom"
    APPEARANCE_OF_SYMPTOM = "appearance_of_symptom"
    MOMENT_OF_DAY = "moment_of_day"
    TIME_OF_YEAR = "time_of_year"
    DURING_AFTER_ACTIVITY = "during_after_activity"
    APPOINTMENT_ALLERGY = "appointment_allergy"
    INSURANCE = "insurance"
    INSURANCE_CATEGORY = "insurance_category"

    # Master table
    MASTER_COUNTRY = "m_country"
    PRODUCT_DATA_TYPE = "m_product_data_type"
    PRODUCT_DATA_FORMAT = "m_product_data_format"
    PRODUCT_STATUS = "m_product_status"
    PRODUCT_DATA_SECURITY_LEVEL = "m_product_data_security_level"
    PRODUCT_ORIGINAL_DATA_UPLOAD_METHOD = "m_product_original_data_upload_method"
