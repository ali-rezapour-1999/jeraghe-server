from django.db import models


class ApplicationId(models.TextChoices):
    USER = "user", "User"
    PROFILE = "profile", "Profile"
    IDEA = "idea", "Idea"
    BLOG = "blog", "Blog"
