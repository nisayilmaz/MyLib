from django.db import models

# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=100)
    genre = models.CharField(max_length=50)
    author = models.CharField(max_length=50)
    isbn = models.CharField(max_length=13)
    location = models.ForeignKey('Library', on_delete=models.CASCADE)
    image = models.ImageField()
    info = models.TextField(null=True, blank=True)
    available = models.BooleanField(default=True)

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