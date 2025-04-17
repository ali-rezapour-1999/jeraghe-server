from threading import local

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
