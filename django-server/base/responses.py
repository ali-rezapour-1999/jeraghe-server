# responses.py
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from django.utils.translation import gettext_lazy as _
import traceback
from .models import ExceptionTrace
from django.http import HttpRequest


def success_response(
    message=None,
    data=None,
    status_code=status.HTTP_200_OK,
    extra=None,
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
    request=None,
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

    if request and isinstance(request, HttpRequest) and status_code >= 400:
        try:
            headers = {}
            for key, value in request.META.items():
                if key.startswith("HTTP_"):
                    headers[key[5:].lower()] = value

            try:
                if request.body:
                    body = request.body.decode("utf-8")
                else:
                    body = None
            except Exception:
                body = None

            ip_address = get_client_ip(request)

            user_id = None
            if hasattr(request, "user") and request.user.is_authenticated:
                user_id = str(request.user.id)

            ExceptionTrace.objects.create(
                path=request.path,
                method=request.method,
                status_code=status_code,
                error_message=message or _("مشکلی در پردازش درخواست وجود دارد."),
                stack_trace=traceback.format_exc() if errors else None,
                request_headers=headers,
                request_body=body,
                user_id=user_id,
                ip_address=ip_address,
                is_from_gateway=False,
            )
        except Exception as e:
            print(f"خطا در ثبت خطا: {e}")

    return Response(response, status=status_code)


def exception_response(
    exception,
    message=None,
    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    error_code="server_error",
    request=None,
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

    if request and isinstance(request, HttpRequest):
        try:
            headers = {}
            for key, value in request.META.items():
                if key.startswith("HTTP_"):
                    headers[key[5:].lower()] = value

            try:
                if request.body:
                    body = request.body.decode("utf-8")
                else:
                    body = None
            except Exception:
                body = None

            ip_address = get_client_ip(request)

            user_id = None
            if hasattr(request, "user") and request.user.is_authenticated:
                user_id = str(request.user.id)

            ExceptionTrace.objects.create(
                path=request.path,
                method=request.method,
                status_code=status_code,
                error_message=str(exception),
                stack_trace=tb,
                request_headers=headers,
                request_body=body,
                user_id=user_id,
                ip_address=ip_address,
                is_from_gateway=False,
            )
        except Exception as e:
            print(f"خطا در ثبت خطا: {e}")

    return Response(response, status=status_code)


def get_client_ip(request):
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0].strip()
    else:
        ip = request.META.get("REMOTE_ADDR")
    return ip
