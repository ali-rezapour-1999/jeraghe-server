# Generated by Django 5.1.3 on 2025-03-02 11:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_alter_post_categories_alter_post_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='show_detail',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.ImageField(blank=True, upload_to='media/blog/%Y/%m/%d/'),
        ),
    ]
