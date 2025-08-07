from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from common.constant.constant import RegexPattern
from common.custom.exceptions import APIError
from common.utils.strings import check_regex


class ForeignKeyUuidField(serializers.CharField):

    def __init__(self, model, **kwargs):
        self.model = model
        super().__init__(**kwargs)

    def to_internal_value(self, data):
        if not data:
            return None

        try:
            obj = self.model.objects.get(uuid=data, is_deleted=False)
        except ObjectDoesNotExist:
            raise serializers.ValidationError("Uuid does_not_exist")
        except (TypeError, ValueError):
            raise serializers.ValidationError("Uuid incorrect_type")

        return obj.id


class ForeignKeyField(serializers.IntegerField):

    def __init__(self, model, **kwargs):
        self.model = model
        super().__init__(**kwargs)

    def to_internal_value(self, data):
        if not data and not self.required:
            return None

        try:
            obj = self.model.objects.get(pk=data)
        except ObjectDoesNotExist:
            raise serializers.ValidationError("Id does_not_exist")
        except (TypeError, ValueError):
            raise serializers.ValidationError("Id incorrect_type")

        return obj.id


class SourceField(serializers.Field):

    def __init__(self, source_list=[], **kwargs):
        kwargs["read_only"] = True
        kwargs["source"] = ".".join(source_list)
        super().__init__(**kwargs)

    def to_representation(self, value):
        return value


class KanaField(serializers.CharField):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def to_internal_value(self, data):
        data = super(KanaField, self).to_internal_value(data)

        if not check_regex(RegexPattern.FULL_NAME_KANA.value, data):
            raise APIError(_("Your full_name_kana is invalid"))

        return data

    def to_representation(self, value):
        return str(value)


class PaginationSerializers(serializers.Serializer):
    page = serializers.IntegerField(default=1)
    page_size = serializers.IntegerField(default=10)
