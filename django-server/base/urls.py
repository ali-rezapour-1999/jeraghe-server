from django.urls import path
from .views import Contact

urlpatterns = [
    path("/", CategoryView.as_view(), name="category"),
]
