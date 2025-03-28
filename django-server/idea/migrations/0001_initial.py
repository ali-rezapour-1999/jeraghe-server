# Generated by Django 5.1.7 on 2025-03-28 18:43

import base.utils
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Idea',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug_id', models.SlugField(blank=True, default=base.utils.generate_unique_id, editable=False, help_text='Unique identifier for the object', max_length=255, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Timestamp of object creation')),
                ('updated_at', models.DateTimeField(auto_now=True, help_text='Timestamp of last update')),
                ('is_active', models.BooleanField(default=True, help_text='Indicates if the object is active or soft-deleted')),
                ('title', models.CharField(max_length=255)),
                ('image', models.ImageField(blank=True, null=True, upload_to='idea_images/')),
                ('description', models.TextField()),
                ('target_audience', models.TextField(verbose_name='مخاطب هدف')),
                ('requirements', models.TextField(verbose_name='نیازمندی\u200cها')),
                ('status', models.CharField(choices=[('idea', 'ایده خام'), ('development', 'در حال توسعه'), ('prototype', 'نمونه اولیه'), ('funding', 'در حال جذب سرمایه')], default='idea', max_length=50, verbose_name='وضعیت فعلی ایده')),
                ('needs_collaborators', models.BooleanField(default=False, verbose_name='نیاز به همکار داری؟')),
                ('required_skills', models.TextField(blank=True, verbose_name='مهارت\u200cهای مورد نیاز')),
                ('collaboration_type', models.CharField(blank=True, choices=[('full_time', 'تمام\u200cوقت'), ('part_time', 'پاره\u200cوقت'), ('consultant', 'مشاوره\u200cای'), ('equity', 'سهام\u200cمحور')], max_length=50, null=True, verbose_name='نحوه همکاری')),
                ('related_files', models.FileField(blank=True, null=True, upload_to='idea_files/', verbose_name='تصاویر و فایل\u200cهای مرتبط')),
                ('related_links', models.URLField(blank=True, verbose_name='لینک\u200cهای مرتبط')),
                ('contact_info', models.TextField(blank=True, verbose_name='راه\u200cهای ارتباطی')),
            ],
            options={
                'verbose_name': 'ایده',
                'verbose_name_plural': 'ایده\u200cها',
                'ordering': ['-created_at'],
                'abstract': False,
            },
        ),
    ]
