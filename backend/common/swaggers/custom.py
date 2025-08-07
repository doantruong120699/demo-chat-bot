from drf_spectacular.openapi import AutoSchema
from drf_spectacular.utils import OpenApiParameter
from common.constant.view_action import ViewSetAction


class CustomAutoSchema(AutoSchema):
    global_params = [
        OpenApiParameter(
            name="accept-language",
            type=str,
            location=OpenApiParameter.HEADER,
            description="`ko` or `en`. The default value is en",
        )
    ]

    def get_override_parameters(self):
        params = super().get_override_parameters()
        return params + self.global_params

    def _get_pagination_parameters(self):
        if (
            getattr(self.view, "action", None) == ViewSetAction.STATISTICS.value
            or getattr(self.view, "action", None)
            == ViewSetAction.DELETE_WITH_CONDITION.value
        ):
            return []

        return super()._get_pagination_parameters()

    def get_filter_backends(self):
        if (
            getattr(self.view, "action", None) == ViewSetAction.STATISTICS.value
            or getattr(self.view, "action", None)
            == ViewSetAction.DELETE_WITH_CONDITION.value
        ):
            return getattr(self.view, "filter_backends", [])

        return super().get_filter_backends()
