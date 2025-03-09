from django.db import models
from user.models import CustomUser
from base.models import BaseModel, Category
from django.utils import timezone
from base.models import Tags


class Post(BaseModel):
    title = models.CharField(max_length=500, null=False, blank=False)
    user = models.ForeignKey(
        CustomUser, related_name="post_user", on_delete=models.CASCADE
    )
    content = models.TextField()
    status = models.CharField(
        max_length=10,
        choices=[("draft", "Draft"), ("published", "Published")],
        default="draft",
    )
    tags = models.ManyToManyField(Tags, related_name="post_tag", blank=True)
    categories = models.ForeignKey(
        Category,
        on_delete=models.DO_NOTHING,
        related_name="post_category",
        blank=True,
    )
    image = models.ImageField(upload_to="media/blog/%Y/%m/%d/", blank=True)
    views = models.PositiveIntegerField(default=0)
    publish = models.DateTimeField(default=timezone.now)
    show_detail = models.BooleanField(default=True)
    is_approve = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ("-publish",)
        verbose_name = "پست"
        verbose_name_plural = "پست"
