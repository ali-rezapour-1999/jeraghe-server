from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from base.models import Tags
from user.models import CustomUser
from base.models import BaseModel


class Profile(BaseModel):
    user = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, related_name="profil_user"
    )
    gender = models.CharField(max_length=12, blank=True, null=True)
    age = models.PositiveIntegerField(blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    desciption = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.user}"

    class Meta(BaseModel.Meta):
        verbose_name = "Profile"
        verbose_name_plural = "Profile"


class WorkHistory(BaseModel):
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="work_history"
    )
    job_title = models.CharField(max_length=200, blank=True)
    company_name = models.CharField(max_length=200, blank=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(null=True, blank=True)
    job_description = models.TextField(blank=True, null=True)
    is_working = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.job_title} at {self.company_name}"

    class Meta(BaseModel.Meta):
        verbose_name = "WorkHistory"
        verbose_name_plural = "WorkHistory"


class Skill(BaseModel):
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="user_skills"
    )
    skill_reference = models.ForeignKey(
        Tags, on_delete=models.CASCADE, related_name="related_skill"
    )
    year = models.PositiveIntegerField(null=True , blank=True)
    moon = models.PositiveIntegerField(null=True , blank=True)
    level = models.DecimalField(
        max_digits=5,
        decimal_places=1,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        null=True,
        blank=True,
    )

    def __str__(self):
        return f"{self.user} - {self.skill_reference}"

    class Meta(BaseModel.Meta):
        verbose_name = "مهارت های کاربر"
        verbose_name_plural = "مهارت های کاربر"
