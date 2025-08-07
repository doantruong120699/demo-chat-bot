from enum import Enum

from django.utils.translation import gettext_lazy as _

from common.constant.app_label import ModelAppLabel
from common.custom.exceptions import APIError


class MasterDataTable(Enum):
    # name, app_label, table_name, is_create
    COUNTRY = "country", ModelAppLabel.MASTER.value, "CountryMaster", False

    @staticmethod
    def model_name(master_name):
        for v in MasterDataTable.__members__.values():
            if master_name in v.value[0]:
                return v.value[1], v.value[2]

        raise APIError(_("Master model not exist"))

    @staticmethod
    def list(is_create=False):
        master_list = list(
            filter(lambda c: (is_create is False or c.value[3]), MasterDataTable)
        )
        return [x.value[0] for x in master_list]

    @property
    def table_name(self):
        return self.value[2]
