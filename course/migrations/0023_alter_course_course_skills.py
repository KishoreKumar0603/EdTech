# Generated by Django 5.1.2 on 2025-01-02 09:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0022_rename_visibility_course_lock_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='course_skills',
            field=models.CharField(blank=True, max_length=3000, null=True),
        ),
    ]
