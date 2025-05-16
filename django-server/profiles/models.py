from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from user.models import CustomUser
from base.models import BaseModel, Category,  Tags


class Profile(BaseModel):
    user = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, related_name="profil_user")
    gender = models.CharField(max_length=12, blank=True, null=True)
    age = models.CharField(blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    career = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.user}"

    class Meta(BaseModel.Meta):
        verbose_name = "پروفایل"
        verbose_name_plural = "پروفایل"


class ProfileSkill(BaseModel):
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="profile_skill")
    category = models.ForeignKey(Category, on_delete=models.NOT_PROVIDED)

    def __str__(self):
        return f"{self.user} , {self.title}"

    class Meta(BaseModel.Meta):
        verbose_name = "مهارت های پروفایل"
        verbose_name_plural = "مهارت های پروفایل"


class SkillItems(BaseModel):
    profile_skill = models.ForeignKey(
        ProfileSkill, on_delete=models.CASCADE, related_name="skill_items")
    skill = models.ForeignKey(
        Tags, on_delete=models.CASCADE, related_name="related_skill")
    level = models.DecimalField(
        max_digits=5,
        decimal_places=1,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        null=True,
        blank=True,
    )

    def __str__(self):
        return f"{self.profileSkill__user} , {self.skill}"

    class Meta(BaseModel.Meta):
        verbose_name = "مهارت های پروفایل"
        verbose_name_plural = "مهارت های پروفایل"


class Experience(BaseModel):
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
        verbose_name = "Experience"
        verbose_name_plural = "Experience"


class Education(BaseModel):
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="education")
    school = models.CharField(max_length=200)
    degree = models.CharField(max_length=100)
    field_of_study = models.CharField(max_length=100)
    start_year = models.IntegerField()
    end_year = models.IntegerField(blank=True, null=True)
    grade = models.CharField(max_length=10, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.job_title} at {self.company_name}"

    class Meta(BaseModel.Meta):
        verbose_name = "Education"
        verbose_name_plural = "Education"
