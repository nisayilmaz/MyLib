# Generated by Django 4.0.5 on 2022-08-09 12:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('study_group', '0004_studygroup_avatar'),
    ]

    operations = [
        migrations.AddField(
            model_name='studygroup',
            name='slug',
            field=models.SlugField(default='', unique=True),
            preserve_default=False,
        ),
    ]
