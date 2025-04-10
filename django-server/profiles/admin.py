from django.contrib import admin

from .models import Profile, Skill, WorkHistory


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "slug_id", "is_active", "created_at")
    list_filter = ("gender", "state", "city", "is_active")
    search_fields = ("user__email", "user__phone_number")
    readonly_fields = ("created_at", "updated_at", "slug_id")
    fieldsets = (
        (
            "Personal Info",
            {
                "fields": (
                    "slug_id",
                    "user",
                    "age",
                    "gender",
                )
            },
        ),
        ("Address", {"fields": ("state", "city", "address")}),
        ("Professional Info", {"fields": ("description_myself",)}),
        ("Other Info", {"fields": ("is_active", "created_at", "updated_at")}),
    )


@admin.register(WorkHistory)
class WorkHistoryAdmin(admin.ModelAdmin):
    list_display = ("user", "job_title", "company_name", "start_date", "end_date")
    list_filter = ("company_name", "start_date", "end_date")
    search_fields = ("job_title", "company_name")
    date_hierarchy = "start_date"
    readonly_fields = ("created_at", "updated_at", "slug_id")
    fields = (
        "user",
        "job_title",
        "company_name",
        "start_date",
        "end_date",
        "job_description",
    )


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ("user",)
    readonly_fields = ("created_at", "updated_at", "slug_id")
    search_fields = (
        "user",
        "skill",
    )
