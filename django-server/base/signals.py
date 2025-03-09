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


@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


@receiver(pre_save, sender=BaseModel)
def set_user_fields(sender, instance, **kwargs):
    user = None
    if not instance.pk:
        if user:
            instance.create_by = user
    else:
        if user:
            instance.updated_by = user
