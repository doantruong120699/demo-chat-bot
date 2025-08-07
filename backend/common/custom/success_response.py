from rest_framework.response import Response
from rest_framework import status
from django.utils.translation import gettext_lazy as _


def success_response(
    message: str = None, data=None, status_code: int = status.HTTP_200_OK
):
    """
    Custom success response formatter

    Args:
        data: Response data
        message: Success message
        status_code: HTTP status code

    Returns:
        Response: Formatted success response
    """
    response_data = {
        "status_code": "success",
        "message": message or _("Success"),
    }

    if data is not None:
        response_data["data"] = data

    return Response(response_data, status=status_code)
