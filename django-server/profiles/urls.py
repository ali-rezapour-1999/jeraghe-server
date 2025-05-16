from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import (
    ExperienceViewSet,
    ProfileUpdateView,
    ProfileGetView,
    ProfileSkillViewSet
)

router = DefaultRouter()
router.register(r"experience", ExperienceViewSet, basename="experience")
router.register(r"profile-skill", ProfileSkillViewSet,
                basename="profile-skill")

urlpatterns = [
    path("update/", ProfileUpdateView.as_view(), name="profile-update"),
    path("get/", ProfileGetView.as_view(), name="profile-get"),
    path("", include(router.urls)),
]
