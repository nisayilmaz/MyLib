# Generated by Django 4.0.5 on 2022-07-26 09:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0004_book_image_url_alter_book_author_alter_book_image_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='image_url',
            field=models.URLField(blank=True, null=True),
        ),
    ]