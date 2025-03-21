from django.urls import path
from .views import (
    CreatePostView,
    UpdatePostView,
    GetPostView,
    ListPostView,
    UserListPostView,
)

urlpatterns = [
    path("create/", CreatePostView.as_view(), name="create-post"),
    path("update/<int:pk>", UpdatePostView.as_view(), name="update-post"),
    path("get/<int:pk>", GetPostView.as_view(), name="get-post"),
    path("list/", ListPostView.as_view(), name="list-post"),
    path("user-list/", UserListPostView.as_view(), name="user-list-post"),
]
