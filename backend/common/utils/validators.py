from django.core.validators import BaseValidator
from django.utils.deconstruct import deconstructible

from common.constant.message_code import common_message


@deconstructible
class FileSizeValidator(BaseValidator):
    limit_value = 5
    message = str(common_message.MAX_FILE_SIZE).format(value=limit_value)
    code = "invalid_file_size"

    def compare(self, file_size, size_limit):
        return file_size > size_limit * 1024 * 1024

    def clean(self, file_obj):
        return file_obj.size
