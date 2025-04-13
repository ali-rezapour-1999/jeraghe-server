from django.db import models


class ApplicationId(models.TextChoices):
    USER = 0, "user"
    PROFILE = 1, "profile"
    IDEA = 2, "idea"
    BLOG = 3, "blog"
