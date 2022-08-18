from django.db import models
from accounts.models import User


class StudyGroup(models.Model):
    users = models.ManyToManyField(User)
    title = models.CharField(max_length=300, unique=True)
    name = models.CharField(max_length=300,)
    subject = models.TextField()
    avatar = models.ImageField()


class Message(models.Model):
    username = models.CharField(max_length=255)
    room = models.CharField(max_length=255)
    content = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
