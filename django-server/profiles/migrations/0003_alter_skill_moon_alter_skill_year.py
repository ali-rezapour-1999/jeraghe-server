# Generated by Django 5.1.6 on 2025-04-09 19:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='skill',
            name='moon',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='skill',
            name='year',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]
