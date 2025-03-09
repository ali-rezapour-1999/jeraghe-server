from django.utils.translation import gettext_lazy as _
from user.middleware import get_current_user
from django.db import models
from base.utils import generate_unique_id
from user.models import CustomUser


class BaseModel(models.Model):
    slug_id = models.SlugField(
        max_length=255,
        unique=True,
        blank=True,
        default=generate_unique_id,
        editable=False,
    )
    create_by = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="%(class)s_create_by",
    )
    updated_by = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="%(class)s_updated_by",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True


class Tags(BaseModel):
    title = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name = "تگ"
        verbose_name_plural = "تگ"

    def save(self, *args, **kwargs):
        user = get_current_user()
        if not self.pk:
            self.create_by = user
        self.updated_by = user
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Category(BaseModel):
    title = models.CharField(max_length=100, unique=True, verbose_name=_("عنوان"))
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="subcategories",
        verbose_name=_("دسته‌بندی مادر"),
    )

    class Meta:
        verbose_name_plural = "دسته بندی‌ها"
        verbose_name = "دسته بندی"

    def save(self, *args, **kwargs):
        user = get_current_user()
        if not self.pk:
            self.create_by = user
        self.updated_by = user
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
