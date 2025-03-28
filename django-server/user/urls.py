from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView
from .views import (
    UserRegistrationView,
    UserLoginView,
    GetUserInformationView,
    UpdateUserInformationView,
    RequestPasswordReset,
    PasswordResetConfirmView,
)


urlpatterns = [
    path("get/", GetUserInformationView.as_view(), name="user-get"),
    path("update/", UpdateUserInformationView.as_view(), name="user-update"),
    path("register/", UserRegistrationView.as_view(), name="user-register"),
    path("login/", UserLoginView.as_view(), name="user-login"),
    path("token-refresh/", TokenRefreshView.as_view(), name='token_refresh'),
    path("token-verify/", TokenVerifyView.as_view(), name="token-verify"),
    path("reset-password/", RequestPasswordReset.as_view(), name="password_reset"),
    path(
        "reset-password/<uidb64>/<token>/",
        PasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
]
