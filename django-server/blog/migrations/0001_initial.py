# Generated by Django 5.1.6 on 2025-04-08 19:24

import base.utils
import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug_id', models.SlugField(blank=True, default=base.utils.generate_unique_id, editable=False, help_text='Unique identifier for the object', max_length=255, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Timestamp of object creation')),
                ('updated_at', models.DateTimeField(auto_now=True, help_text='Timestamp of last update')),
                ('is_active', models.BooleanField(default=True, help_text='Indicates if the object is active or soft-deleted')),
                ('title', models.CharField(max_length=500)),
                ('content', models.TextField()),
                ('status', models.CharField(choices=[('draft', 'Draft'), ('published', 'Published')], default='draft', max_length=10)),
                ('image', models.ImageField(blank=True, null=True, upload_to='media/blog/%Y/%m/%d/')),
                ('views', models.PositiveIntegerField(default=0)),
                ('publish', models.DateTimeField(default=django.utils.timezone.now)),
                ('show_detail', models.BooleanField(default=True)),
                ('is_approve', models.BooleanField(default=False)),
                ('categories', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='post_category', to='base.category')),
            ],
            options={
                'verbose_name': 'پست',
                'verbose_name_plural': 'پست',
                'ordering': ('-publish',),
                'abstract': False,
            },
        ),
    ]
