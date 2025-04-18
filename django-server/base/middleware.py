from threading import local
import traceback
from django.utils.deprecation import MiddlewareMixin

_user = local()


class CurrentUserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        _user.value = request.user if request.user.is_authenticated else None
        response = self.get_response(request)
        return response


def get_current_user():
    return getattr(_user, "value", None)


class AppTrackerMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path_parts = request.path.strip("/").split("/")
        if len(path_parts) >= 3 and path_parts[0] == "api":
            request.application_id = path_parts[2]
        else:
            request.application_id = None

        return self.get_response(request)


class ErrorLoggingMiddleware(MiddlewareMixin):
    def process_exception(self, request, exception):
        try:
            from base.models import ExceptionTrace

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

            ip_address = self.get_client_ip(request)

            user_id = None
            if hasattr(request, "user") and request.user.is_authenticated:
                user_id = str(request.user.id)
            ExceptionTrace.objects.create(
                path=request.path,
                method=request.method,
                status_code=500,
                error_message=str(exception),
                stack_trace=traceback.format_exc(),
                request_headers=headers,
                request_body=body,
                user_id=user_id,
                ip_address=ip_address,
                is_from_gateway=False,
            )
        except Exception as e:
            print(f"Error logging exception: {e}")
        return None

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0].strip()
        else:
            ip = request.META.get("REMOTE_ADDR")
        return ip
