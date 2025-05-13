from django.db import models


class StatusIdea(models.TextChoices):
    IDEA = "idea", "ایده خام"
    DEVELOPMENT = "development", "در حال توسعه"
    PROTOTYPE = "prototype", "نمونه اولیه"
    FUNDING = "funding", "در حال جذب سرمایه"


class CollaborationType(models.TextChoices):
    FULL_TIME = "full_time", "تمام‌وقت"
    PART_TIME = "part_time", "پاره‌وقت"
    CONSULTANT = "consultant", "مشاوره‌ای"
    PARTICIPATORY = "participatory", "مشارکتی"
