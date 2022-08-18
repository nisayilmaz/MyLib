from django.contrib import admin

# Register your models here.
from .models import StudyGroup, Message

admin.site.register(StudyGroup)
admin.site.register(Message)