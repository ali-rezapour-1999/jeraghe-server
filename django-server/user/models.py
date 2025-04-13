from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
)
from .manager import CustomUserManager
from django.db import models
from base.utils import validate_iranian_phone_number


class CustomUser(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = [
        ("admin", "Admin"),
        ("user", "User"),
        ("editor", "Editor"),
        ("manager", "Manager"),
    ]
    slug_id = models.CharField(max_length=255, unique=True, blank=True)
    email = models.EmailField(unique=True)
    image = models.ImageField(upload_to="media/blog/%Y/%m/%d/", blank=True, null=True)
    phone_number = models.CharField(
        max_length=11,
        unique=True,
        blank=True,
        null=True,
        validators=[validate_iranian_phone_number],
    )
    username = models.CharField(max_length=100, null=False, blank=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default="user")

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta(PermissionsMixin.Meta, AbstractBaseUser.Meta):
        verbose_name = "User"
        verbose_name_plural = "User"


class TokenLog(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    access_token = models.TextField()
    refresh_token = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    def __str__(self):
        return f"Token for {self.user.email}"
