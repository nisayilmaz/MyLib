from django.db import models
from django.core.files import File
from urllib.request import urlopen
from tempfile import NamedTemporaryFile
import os
from django.template.defaultfilters import slugify


# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=400)
    author = models.CharField(max_length=200)
    isbn = models.CharField(max_length=13)
    location = models.ForeignKey('Library', on_delete=models.CASCADE)
    image = models.ImageField()
    info = models.TextField(null=True, blank=True)
    available = models.BooleanField(default=True)
    image_src = models.CharField(max_length=300, null=True, blank=True)

    def save(self, *args, **kwargs):
        string = self.title
        slug = slugify(string)
        if self.image_src and not self.image:
            img_temp = NamedTemporaryFile(delete=True)
            img_temp.write(urlopen(self.image_src).read())
            img_temp.flush()
            self.image.save(f"{slug}.jpg", File(img_temp))
        super(Book, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


class Library(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    phone = models.CharField(max_length=11)
    image = models.ImageField()
    email = models.EmailField()

    def __str__(self):
        return self.name


class Borrowed(models.Model):
    borrowed_by = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    book = models.ForeignKey('Book', on_delete=models.CASCADE)
    borrow_date = models.DateField()
    latest_return_date = models.DateField()
    returned = models.DateField(null=True, blank=True)
