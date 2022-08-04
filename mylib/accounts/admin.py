from django.contrib import admin
from .models import User, FriendRequest, Profile

# Register your models here.
admin.site.register(User)
admin.site.register(FriendRequest)
admin.site.register(Profile)