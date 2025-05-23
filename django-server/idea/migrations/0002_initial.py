# Generated by Django 5.1.6 on 2025-04-08 19:24

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('base', '0002_initial'),
        ('idea', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='idea',
            name='created_by',
            field=models.ForeignKey(blank=True, help_text='User who created this object', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(app_label)s_%(class)s_created_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='idea',
            name='tags',
            field=models.ManyToManyField(blank=True, related_name='idea_tags', to='base.tags'),
        ),
        migrations.AddField(
            model_name='idea',
            name='updated_by',
            field=models.ForeignKey(blank=True, help_text='User who last updated this object', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(app_label)s_%(class)s_updated_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='idea',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ideas', to=settings.AUTH_USER_MODEL),
        ),
    ]
