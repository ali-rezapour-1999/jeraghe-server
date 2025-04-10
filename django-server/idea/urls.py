from django.urls import path
from .views import CreateIdeaView, UpdateIdeaView


urlpatterns = [
    path("create/", CreateIdeaView.as_view(), name="create-idea"),
    path("update/", UpdateIdeaView.as_view(), name="update-idea"),
]
