from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import (
    ProfileViewSet,
    UserSkillViewSet,
    WorkHistoryViewSet,
    SocialMediaViewSet,
)

router = DefaultRouter()
router.register(r"profile-info", ProfileViewSet, basename="profiles")
router.register(r"work-history", WorkHistoryViewSet, basename="work-history")
router.register(r"social-media", SocialMediaViewSet, basename="social-media")
router.register(r"user-skills", UserSkillViewSet, basename="user-skills")

urlpatterns = [
    path("", include(router.urls)),
]
