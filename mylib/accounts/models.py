from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    library = models.ForeignKey('library.Library', on_delete=models.CASCADE, blank=True, null=True)
    friends = models.ManyToManyField("User", blank=True)
    avatar = models.ImageField(default=None, null=True, blank=True, upload_to='profile_images')


class Profile(models.Model):
    user = models.OneToOneField('User', on_delete=models.CASCADE)
    bio = models.TextField(null=True, blank=True)


class FriendRequest(models.Model):
    from_user = models.ForeignKey(User, related_name='from_user', on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name='to_user', on_delete=models.CASCADE)
