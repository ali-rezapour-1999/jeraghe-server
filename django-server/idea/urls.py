from django.urls import path
from .views import CreateIdeaView, DeleteIdeaView, GetIdeaView, UpdateIdeaView


urlpatterns = [
    path("create/", CreateIdeaView.as_view(), name="create-idea"),
    path("update/", UpdateIdeaView.as_view(), name="update-idea"),
    path("delete/", DeleteIdeaView.as_view(), name="delete-idea"),
    path("get/", GetIdeaView.as_view(), name="get-idea"),
]
