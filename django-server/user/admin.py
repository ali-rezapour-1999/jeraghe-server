from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import CustomUser, TokenLog


@admin.register(CustomUser)
class CustomUserAdmin(BaseUserAdmin):
    fieldsets = (
        (
            None,
            {"fields": ("slug_id", "email", "username", "password", "role")},
        ),
        (_("Personal info"), {"fields": ("phone_number", "image")}),
        (_("Permissions"), {"fields": ("is_active", "is_staff", "is_superuser")}),
        (_("Important dates"), {"fields": ("last_login",)}),
    )
    readonly_fields = (
        "created_at",
        "slug_id",
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2"),
            },
        ),
    )
    list_display = ("email", "slug_id", "is_staff", "is_active")
    search_fields = ("email",)
    ordering = ("email",)


@admin.register(TokenLog)
class TokenLogAdmin(admin.ModelAdmin):
    list_display = ("user", "access_token", "refresh_token", "created_at", "expires_at")
    list_filter = ("user", "created_at")
    search_fields = ("user__email", "access_token", "refresh_token")
    ordering = ("-created_at",)
    date_hierarchy = "created_at"
    readonly_fields = (
        "user",
        "access_token",
        "refresh_token",
        "created_at",
        "expires_at",
    )
