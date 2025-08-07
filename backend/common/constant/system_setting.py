from enum import unique, Enum
from common.constant.app_label import ModelAppLabel
from django.conf import settings


@unique
class SystemSettingEnum(Enum):
    SYSTEM_NAME = "system_name", f"{settings.WEBSITE_NAME}"
    SYSTEM_LOGO_URL = "system_logo_url", ""
    SYSTEM_FAVICON_URL = "system_favicon_url", ""
    SYSTEM_BACKGROUND_URL = "system_background_url", ""

    @staticmethod
    def list():
        master_list = list(filter(lambda c: c.value[0], SystemSettingEnum))
        return [(x.value[0], x.value[1]) for x in master_list]

    @staticmethod
    def options():
        master_list = list(filter(lambda c: c.value[0], SystemSettingEnum))
        return [x.value[0] for x in master_list]

    @staticmethod
    def get_name(self):
        return self.value[0]

    @staticmethod
    def get_value(self):
        return self.value[1]
