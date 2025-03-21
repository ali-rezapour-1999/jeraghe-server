# Generated by Django 5.1.6 on 2025-03-21 08:18

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0003_alter_socialmedia_address'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='description_myself',
            new_name='desciption',
        ),
        migrations.AlterField(
            model_name='profile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profil_user', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='socialmedia',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='socila_media', to=settings.AUTH_USER_MODEL),
        ),
    ]
