from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import PostViewSet, UserPostViewSet

router = DefaultRouter()
router.register("view-post", PostViewSet, basename="post")
router.register("user-post", UserPostViewSet, basename="user-post")

urlpatterns = [
    path("", include(router.urls)),
]
