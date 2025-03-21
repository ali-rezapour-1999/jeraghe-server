from .models import CustomUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from profiles.models import Profile
from base.models import BaseModel
from django.db.models.signals import pre_save


@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
