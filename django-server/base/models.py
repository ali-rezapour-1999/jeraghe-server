from django.db.models.query import timezone
from django.utils.translation import gettext_lazy as _
from django.db import models
from .utils import generate_unique_id
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
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="%(app_label)s_%(class)s_created_by",
        help_text="User who created this object",
    )
    updated_by = models.ForeignKey(
        CustomUser,
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
    is_active = models.BooleanField(default=True)  # type: ignore
    application_id = models.CharField(max_length=255, editable=False)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        abstract = True
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):
        user = get_current_user()
        if user and hasattr(user, "pk") and user.pk:
            if not self.pk:
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
    title = models.CharField(
        max_length=100, unique=True, verbose_name=_("عنوان"))
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
    is_verified = models.BooleanField(
        default=False, verbose_name="تایید شده؟")  # type: ignore

    def __str__(self):
        return f"{self.user.username} - {self.platform}"

    class Meta(BaseModel.Meta):
        verbose_name = "اطلاعات تماس شبکه اجتماعی"
        verbose_name_plural = "اطلاعات تماس شبکه‌های اجتماعی"


class ExceptionTrace(models.Model):
    timestamp = models.DateTimeField(default=timezone.now)
    path = models.CharField(max_length=255, null=True, blank=True)
    method = models.CharField(max_length=10, null=True, blank=True)
    status_code = models.IntegerField(null=True, blank=True)
    error_message = models.TextField(null=True, blank=True)
    stack_trace = models.TextField(null=True, blank=True)
    request_headers = models.JSONField(null=True, blank=True)
    request_body = models.TextField(null=True, blank=True)
    user_id = models.CharField(max_length=100, null=True, blank=True)
    ip_address = models.CharField(max_length=45, null=True, blank=True)
    is_from_gateway = models.BooleanField(default=False)

    class Meta:
        db_table = "exception_traces"
        ordering = ["-timestamp"]

    def __str__(self):
        return f"{self.status_code} - {self.path} - {self.timestamp}"
