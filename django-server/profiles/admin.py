from django.contrib import admin

from .models import Profile, ProfileSkill, SkillItems, Experience


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
        ("Professional Info", {"fields": ("description",)}),
        ("Other Info", {"fields": ("is_active", "created_at", "updated_at")}),
    )


@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ("user", "job_title", "company_name",
                    "start_date", "end_date")
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


@admin.register(ProfileSkill)
class ProfileSkillAdmin(admin.ModelAdmin):
    list_display = ("user",)
    readonly_fields = ("created_at", "updated_at", "slug_id")
    search_fields = (
        "user",
        "category",
    )


@admin.register(SkillItems)
class SkillItemsAdmin(admin.ModelAdmin):
    list_display = ("profile_skill", 'skill', 'level')
    readonly_fields = ("created_at", "updated_at", "slug_id")
    search_fields = (
        "profile_skill",
        "skill",
        "level",
    )
