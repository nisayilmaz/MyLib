# Generated by Django 4.0.5 on 2022-07-26 10:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0007_alter_book_image_alter_book_image_url'),
    ]

    operations = [
        migrations.RenameField(
            model_name='book',
            old_name='image_url',
            new_name='image_src',
        ),
    ]
