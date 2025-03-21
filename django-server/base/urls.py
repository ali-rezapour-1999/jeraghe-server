from django.urls import path
from .views import CategoryView

urlpatterns = [
    path("category-list", CategoryView.as_view(), name="category"),
]
