# Generated by Django 4.0.5 on 2022-07-27 13:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0008_rename_image_url_book_image_src'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='image',
            field=models.ImageField(default='static/img/bos.png', upload_to=''),
        ),
    ]
