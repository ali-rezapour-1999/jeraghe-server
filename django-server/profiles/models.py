from django.db import models
from user.models import CustomUser
from base.models import BaseModel, Skill


class Profile(BaseModel):
    user = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, related_name="profil_user"
    )
    gender = models.CharField(max_length=12, blank=True, null=True)
    age = models.PositiveIntegerField(blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.user}"

    class Meta(BaseModel.Meta):
        verbose_name = "Profile"
        verbose_name_plural = "Profile"


class ProfileSkill(BaseModel):
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="user_skill"
    )
    profile = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name="profile_skill"
    )
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE, related_name="skill")

    def __str__(self):
        return f"{self.user} at {self.profile} {self.skill}"

    class Meta(BaseModel.Meta):
        verbose_name = "مهارت های من"
        verbose_name_plural = "مهارت های من"


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
