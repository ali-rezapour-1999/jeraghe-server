from django.urls import path
from .views import ContactCreateView


urlpatterns = [
    path("create-contact/", ContactCreateView.as_view(), name="create-contact"),
]
