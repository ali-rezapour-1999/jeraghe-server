from django.db import models
from base.models import BaseModel, Category, Tags
from user.models import CustomUser


class Idea(BaseModel):
    status_choices = [
        ("idea", "ایده خام"),
        ("development", "در حال توسعه"),
        ("prototype", "نمونه اولیه"),
        ("funding", "در حال جذب سرمایه"),
    ]

    collaboration_type_choices = [
        ("full_time", "تمام‌وقت"),
        ("part_time", "پاره‌وقت"),
        ("consultant", "مشاوره‌ای"),
        ("participatory", "مشارکتی"),
    ]

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="ideas")
    title = models.CharField(max_length=255, null=False, blank=False)
    image = models.ImageField(upload_to="idea_images/", null=True, blank=True)
    description = models.TextField()
    status = models.CharField(
        max_length=50,
        choices=status_choices,
        verbose_name="وضعیت فعلی ایده",
        blank=False,
        null=False,
        default="idea",
    )
    needs_collaborators = models.BooleanField(
        default=False, verbose_name="نیاز به همکار داری؟"
    )
    required_skills = models.TextField(verbose_name="مهارت‌های مورد نیاز", blank=True)
    collaboration_type = models.CharField(
        max_length=50,
        choices=collaboration_type_choices,
        verbose_name="نحوه همکاری",
        blank=True,
        null=True,
    )
    related_files = models.FileField(
        upload_to="idea_files/",
        verbose_name="تصاویر و فایل‌های مرتبط",
        blank=True,
        null=True,
    )
    related_links = models.URLField(
        max_length=200, verbose_name="لینک‌های مرتبط", blank=True
    )
    tags = models.ManyToManyField(Tags, related_name="idea_tags", blank=True)
    category = models.ForeignKey(
        Category, related_name="idea_category", on_delete=models.DO_NOTHING
    )
    contact_info = models.TextField(verbose_name="راه‌های ارتباطی", blank=True)

    def __str__(self):
        return f"{self.title} - {self.user}"

    class Meta(BaseModel.Meta):
        verbose_name = "ایده"
        verbose_name_plural = "ایده‌ها"
