from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/private/auth/", include("user.urls")),
    path("api/private/profile/", include("profiles.urls")),
    path("api/private/blog/", include("blog.urls")),
    path("api/private/base/", include("base.urls")),
    path("api/private/idea/", include("idea.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
