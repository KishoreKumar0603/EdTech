# Generated by Django 5.1.2 on 2025-01-26 17:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0029_alter_course_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='slug',
            field=models.SlugField(blank=True, unique=True),
        ),
    ]
