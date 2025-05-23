# Generated by Django 5.1.6 on 2025-04-09 19:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('idea', '0003_remove_idea_readme_content_remove_idea_related_links_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='idea',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='idea/idea_images/%Y/%m/%d/'),
        ),
        migrations.AlterField(
            model_name='idea',
            name='related_files',
            field=models.FileField(blank=True, null=True, upload_to='idea/idea_files/%Y/%m/%d/', verbose_name='فایل\u200cهای مرتبط'),
        ),
    ]
