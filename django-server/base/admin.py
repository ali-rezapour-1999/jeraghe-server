from django.contrib import admin
from .models import Tags, Category


@admin.register(Tags)
class TagsAdmin(admin.ModelAdmin):
    list_display = ("title",)
    search_fields = ("title",)
    readonly_fields = ("created_at", "updated_at", "slug_id")
    ordering = ("title",)


@admin.register(Category)
class CatagoryMediaAdmin(admin.ModelAdmin):
    list_display = ("slug_id", "is_active", "created_at")
    list_filter = ("title", "is_active")
    readonly_fields = ("created_at", "updated_at", "slug_id")
    fieldsets = (
        (
            "Personal Info",
            {"fields": ("slug_id", "title")},
        ),
        ("Other Info", {"fields": ("is_active", "created_at", "updated_at")}),
    )
