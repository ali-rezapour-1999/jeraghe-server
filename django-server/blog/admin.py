from django.contrib import admin
from .models import Post


@admin.register(Post)
class SocialMediaAdmin(admin.ModelAdmin):
    list_display = ("user", "slug_id", "is_active", "created_at")
    list_filter = ("status", "categories", "tags", "user", "is_active")
    search_fields = (
        "user__email",
        "user__phone_number",
    )
    readonly_fields = ("created_at", "updated_at", "slug_id", "views")
    fieldsets = (
        (
            "Personal Info",
            {
                "fields": (
                    "slug_id",
                    "user",
                    "categories",
                    "tags",
                    "views",
                    "image",
                    "show_detail",
                    "is_approve",
                )
            },
        ),
        (
            "Post",
            {"fields": ("title", "content", "publish", "status")},
        ),
        ("Other Info", {"fields": ("is_active", "created_at", "updated_at")}),
    )
