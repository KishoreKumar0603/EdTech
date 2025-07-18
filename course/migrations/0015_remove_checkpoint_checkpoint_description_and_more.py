
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0014_remove_course_checkpoint_description_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='checkpoint',
            name='checkpoint_description',
        ),
        migrations.RemoveField(
            model_name='checkpoint',
            name='checkpoint_duration',
        ),
        migrations.RemoveField(
            model_name='checkpoint',
            name='checkpoint_title',
        ),
        migrations.RemoveField(
            model_name='checkpoint',
            name='technology_used',
        ),
        migrations.RemoveField(
            model_name='course',
            name='checkpoint_no',
        ),
        migrations.AddField(
            model_name='course',
            name='checkpoint_description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='course',
            name='checkpoint_duration',
            field=models.CharField(default='check point duration', max_length=30),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='course',
            name='checkpoint_title',
            field=models.CharField(default='check point title', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='course',
            name='technology_used',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
