from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class User(AbstractUser):
    library_address = models.CharField(max_length=300, null=True, blank=True)
    phone = models.CharField(max_length=13, unique=True)


