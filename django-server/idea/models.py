from django.db import models
from base.models import BaseModel, Category, Tags, Contact
from user.models import CustomUser
from profiles.models import Skill


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
    image = models.ImageField(
        upload_to="idea/idea_images/%Y/%m/%d/", null=True, blank=True
    )
    description = models.TextField()
    status = models.CharField(
        max_length=50,
        choices=status_choices,
        verbose_name="وضعیت فعلی ایده",
        blank=False,
        null=False,
        default="idea",
    )
    needs_collaborators = models.BooleanField(verbose_name="نیاز به همکار داری؟")
    required_skills = models.ManyToManyField(
        Skill, related_name="required_skills", verbose_name="مهارت های مورد نیاز"
    )
    collaboration_type = models.CharField(
        max_length=50,
        choices=collaboration_type_choices,
        verbose_name="نحوه همکاری",
        blank=True,
        null=True,
    )
    related_files = models.FileField(
        upload_to="idea/idea_files/%Y/%m/%d/",
        verbose_name="فایل‌های مرتبط",
        blank=True,
        null=True,
    )
    tags = models.ManyToManyField(Tags, related_name="idea_tags", blank=True)
    category = models.ForeignKey(
        Category, related_name="idea_category", on_delete=models.DO_NOTHING
    )
    repo_url = models.URLField()
    contact_info = models.ForeignKey(Contact, on_delete=models.DO_NOTHING)

    def __str__(self):
        return f"{self.title} - {self.user}"

    class Meta(BaseModel.Meta):
        verbose_name = "ایده"
        verbose_name_plural = "ایده‌ها"
