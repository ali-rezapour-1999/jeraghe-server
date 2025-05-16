from django.db import models
from base.models import BaseModel, Category, Tags, Contact
from idea.enum import CollaborationType, StatusIdea
from user.models import CustomUser


class Idea(BaseModel):
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="ideas")
    title = models.CharField(max_length=255, null=False, blank=False)
    log_image = models.ImageField(
        upload_to="idea/idea_images/banner/%Y/%m/%d/", null=True, blank=True
    )
    banner_image = models.ImageField(
        upload_to="idea/idea_images/logo/%Y/%m/%d/", null=True, blank=True
    )
    description = models.TextField()
    status = models.CharField(
        max_length=50,
        choices=StatusIdea.choices,
        verbose_name="وضعیت فعلی ایده",
        blank=False,
        null=False,
        default="idea",
    )
    needs_collaborators = models.BooleanField(
        verbose_name="نیاز به همکار داری؟")
    required_skills = models.ManyToManyField(
        Tags, related_name="required_skills", verbose_name="مهارت های مورد نیاز"
    )
    collaboration_type = models.CharField(
        max_length=50,
        choices=CollaborationType.choices,
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
