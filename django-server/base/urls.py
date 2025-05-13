from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import ContactCreateView, SkillViewSet

router = DefaultRouter()
router.register(r"user-skills", SkillViewSet, basename="user-skills")

urlpatterns = [
    path("create-contact/", ContactCreateView.as_view(), name="create-contact"),
]
