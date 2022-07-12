from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    library = models.ForeignKey('library.Library', on_delete=models.CASCADE, blank=True, null=True)
