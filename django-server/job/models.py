from django.db import models
from user.models import CustomUser
from base.models import BaseModel, Tags


class Job(BaseModel):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="jobs")
    title = models.CharField(max_length=255, null=False, blank=True)
    job_image = models.ImageField(upload_to="job_images/", null=True, blank=True)
    description = models.TextField()
    time = models.IntegerField()
    is_approve = models.BooleanField(default=False)
    is_register = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title} - {self.user}"

    class Meta:
        verbose_name = "ایده ها"
        verbose_name_plural = "ایده ها"


class SkillNeeded(BaseModel):
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name="skills")
    tags = models.ManyToManyField(Tags, related_name="jobs")

    def __str__(self):
        return f"{self.title} - {self.job.title}"

    class Meta:
        verbose_name = "مهارت های مورد نیاز"
        verbose_name_plural = "مهارت های مورد نیاز"
