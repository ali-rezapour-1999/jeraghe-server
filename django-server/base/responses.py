from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from django.utils.translation import gettext_lazy as _
import traceback


def success_response(
    message=None, data=None, status_code=status.HTTP_200_OK, extra=None
):
    response = {
        "status": "success",
        "message": message or _("عملیات با موفقیت انجام شد."),
        "data": data,
    }

    if extra and isinstance(extra, dict):
        response.update(extra)

    return Response(response, status=status_code)


def error_response(
    message=None,
    errors=None,
    status_code=status.HTTP_400_BAD_REQUEST,
    error_code=None,
    extra=None,
):
    response = {
        "status": "error",
        "message": message or _("مشکلی در پردازش درخواست وجود دارد."),
        "errors": errors,
    }

    if error_code:
        response["error_code"] = error_code

    if extra and isinstance(extra, dict):
        response.update(extra)

    return Response(response, status=status_code)


def exception_response(
    exception,
    message=None,
    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    error_code="server_error",
):
    tb = None
    if settings.DEBUG:
        tb = traceback.format_exc()

    response = {
        "status": "error",
        "message": message or _("خطایی سمت سرور رخ داده است."),
        "error": str(exception),
        "error_code": error_code,
    }

    if tb:
        response["traceback"] = tb

    return Response(response, status=status_code)
