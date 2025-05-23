from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import (
    ProfileUpdateView,
    ProfileGetView,
    SkillViewSet,
    WorkHistoryViewSet,
)

router = DefaultRouter()
router.register(r"work-history", WorkHistoryViewSet, basename="work-history")
router.register(r"user-skills", SkillViewSet, basename="user-skills")

urlpatterns = [
    path("update/", ProfileUpdateView.as_view(), name="profile-update"),
    path("get/", ProfileGetView.as_view(), name="profile-get"),
    path("", include(router.urls)),
]
