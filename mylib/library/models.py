from django.db import models


# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=50)
    isbn = models.CharField(max_length=13)
    location = models.ForeignKey('Library', on_delete=models.CASCADE)
    borrow_date = models.DateField(null=True, blank=True)
    return_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.title


class Library(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    image = models.ImageField()

    def __str__(self):
        return self.name
