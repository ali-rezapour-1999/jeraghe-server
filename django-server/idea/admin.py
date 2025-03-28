from django.contrib import admin
from .models import Idea


@admin.register(Idea)
class IdeaAdmin(admin.ModelAdmin):
    list_display = ("title", "user", "status", "needs_collaborators", "created_at")
    list_filter = ("status", "needs_collaborators")
    search_fields = ("title", "description", "target_audience")
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
                    "target_audience",
                    "requirements",
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
        ("فایل‌ها و لینک‌ها", {"fields": ("related_files", "related_links")}),
        ("تگ‌ها و اطلاعات تماس", {"fields": ("tags", "contact_info")}),
        ("وضعیت ایده", {"fields": ("status", "image")}),
    )
    filter_horizontal = ("tags",)
