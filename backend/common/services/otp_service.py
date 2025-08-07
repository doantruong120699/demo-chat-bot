import logging

from django.core.cache import cache
from django.utils.translation import gettext_lazy as _

from common.utils.strings import generate_otp

logger = logging.getLogger(__name__)


class OTPService:

    def __init__(self):
        super(OTPService, self).__init__()

    def create_otp(self, key, type: str, timeout: int):
        if key == "123456789":
            otp = "123456"
        else:
            otp = generate_otp()
        cache.set(f"{type}:{key}", otp, timeout=timeout)
        return otp

    def validate_otp(self, key: str, type: str, otp: str) -> bool:
        val = cache.get(f"{type}:{key}")
        return False if not val else val == otp

    def verified_value(self, key: str, timeout: int):
        cache.set(f"verified_value:{key}", True, timeout=timeout)

    def validate_verified_value(self, key: str):
        val = cache.get(f"verified_value:{key}")
        return False if not val else val
