from django.contrib import admin
from .models import Idea


@admin.register(Idea)
class IdeaAdmin(admin.ModelAdmin):
    list_display = ("title", "user", "status", "needs_collaborators", "created_at")
    list_filter = ("status", "needs_collaborators")
    search_fields = ("title", "description")
    ordering = ("-created_at",)
    date_hierarchy = "created_at"
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "title",
                    "user",
                    "description",
                    "category"
                )
            },
        ),
        (
            "تنظیمات همکاری",
            {
                "fields": (
                    "needs_collaborators",
                    "required_skills",
                    "collaboration_type",
                )
            },
        ),
        ("فایل‌ها و لینک‌ها", {"fields": ("repo_url", "related_files")}),
        ("تگ‌ها و اطلاعات تماس", {"fields": ("tags", "contact_info")}),
        ("وضعیت ایده", {"fields": ("status", "image")}),
    )
    filter_horizontal = ("tags",)
