import logging
import traceback

from django.conf import settings
from django.http import JsonResponse
from django.utils.translation import gettext_lazy as _
from rest_framework import exceptions, status
from rest_framework.response import Response
from rest_framework.views import exception_handler, set_rollback
from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.exceptions import APIException, NotFound
from rest_framework_simplejwt.exceptions import AuthenticationFailed


logger = logging.getLogger(__name__)


def server_error(exc):
    """
    Generic 500 error handler.
    """
    data = {
        "status_code": "error",
        "message": _("Internal Service error"),
        "detail": f"Server Error: {str(exc)}",
    }
    exc_fmt = traceback.format_exc()
    if settings.DEBUG:
        logger.error(repr(exc))
        logger.error(exc_fmt)
        data["exception"] = repr(exc)
        data["traceback"] = exc_fmt
    return JsonResponse(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if not response:
        return server_error(exc)
    elif response is not None and isinstance(exc, exceptions.APIException):
        headers = {}

        if getattr(exc, "auth_header", None):
            headers["WWW-Authenticate"] = exc.auth_header
        if getattr(exc, "wait", None):
            headers["Retry-After"] = "%d" % exc.wait

        data = {
            "status_code": exc.default_code,
            "message": (
                exc.default_detail
                if isinstance(exc.detail, (list, dict))
                else exc.detail
            ),
            "detail": exc.detail,
        }

        if hasattr(exc, "message_level") and getattr(exc, "message_level"):
            data["message_level"] = exc.message_level

        set_rollback()
        logger.warning(f"API bad request {exc}")
        return Response(data, status=exc.status_code, headers=headers)
    else:
        response.data["status_code"] = response.status_code

    return response


class APIError(APIException):
    def __init__(self, detail=None, code=None, message_level=None):
        super().__init__(detail, code)
        self.message_level = message_level

    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = _("Invalid input.")
    default_code = "invalid"


class PermissionDenied(APIException):
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = _("permission denied")
    default_code = "403"


class CustomerInvalidToken(AuthenticationFailed):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = _("Token is invalid or expired")
    default_code = "token_not_valid"
