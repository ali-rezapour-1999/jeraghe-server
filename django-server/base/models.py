from django.utils.translation import gettext_lazy as _
from django.db import models
from base.utils import generate_unique_id
from user.models import CustomUser
from base.middleware import get_current_user


class BaseModel(models.Model):
    slug_id = models.SlugField(
        max_length=255,
        unique=True,
        blank=True,
        default=generate_unique_id,
        editable=False,
        help_text="Unique identifier for the object",
    )
    created_by = models.ForeignKey(
        "user.CustomUser",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="%(app_label)s_%(class)s_created_by",
        help_text="User who created this object",
    )
    updated_by = models.ForeignKey(
        "user.CustomUser",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="%(app_label)s_%(class)s_updated_by",
        help_text="User who last updated this object",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Timestamp of object creation",
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="Timestamp of last update",
    )
    is_active = models.BooleanField(
        default=True,
        help_text="Indicates if the object is active or soft-deleted",
    )

    class Meta:
        abstract = True
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):
        user = get_current_user()
        # فقط اگه کاربر معتبر و ذخیره‌شده باشه تنظیم می‌کنیم
        if user and hasattr(user, "pk") and user.pk:
            if not self.pk:  # فقط موقع ساخت
                self.created_by = user
            self.updated_by = user
        if not self.slug_id:
            self.slug_id = generate_unique_id()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.__class__.__name__} ({self.slug_id})"


class Tags(BaseModel):
    title = models.CharField(max_length=100)

    class Meta(BaseModel.Meta):
        verbose_name = "تگ"
        verbose_name_plural = "تگ"

    def save(self, *args, **kwargs):
        user = CustomUser()
        if not self.pk:
            self.created_by = user
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

    class Meta(BaseModel.Meta):
        verbose_name = "دسته‌بندی‌ها"
        verbose_name_plural = "دسته‌بندی‌ها"

    def save(self, *args, **kwargs):
        user = get_current_user()
        if not self.pk:
            self.created_by = user
        self.updated_by = user
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Contact(BaseModel):
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="contacts"
    )
    platform = models.CharField(max_length=20, verbose_name="شبکه اجتماعی")
    link = models.CharField(max_length=255, verbose_name="نام کاربری یا لینک")
    is_verified = models.BooleanField(default=False, verbose_name="تایید شده؟")

    def __str__(self):
        return f"{self.user.username} - {self.platform}"

    class Meta(BaseModel.Meta):
        verbose_name = "اطلاعات تماس شبکه اجتماعی"
        verbose_name_plural = "اطلاعات تماس شبکه‌های اجتماعی"
