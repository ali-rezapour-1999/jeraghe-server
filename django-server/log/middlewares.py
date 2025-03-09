import traceback
from django.utils.deprecation import MiddlewareMixin
from .models import ErrorLog


class ExceptionLoggingMiddleware(MiddlewareMixin):
    def process_exception(self, request, exception):
        error_traceback = traceback.format_exc()

        ErrorLog.objects.create(
            request_path=request.path,
            request_method=request.method,
            request_body=request.body.decode("utf-8") if request.body else None,
            response_status=500,
            response_message=str(exception),
            traceback_info=error_traceback,
        )
