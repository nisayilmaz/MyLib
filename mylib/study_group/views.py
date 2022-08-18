from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect

# Create your views here.
from django.views import View
from .models import StudyGroup, Message


class StudyGroupView(View):
    def get(self, request, title):
        room = StudyGroup.objects.get(title=title)
        user = request.user
        # Get the messages from the database
        messages = Message.objects.filter(room=title)[0:25]

        # Add the messages to the context

        return render(request, 'study_group/study_group_home.html', {'room': room, 'user': user, 'messages': messages})


class ListStudyGroupView(View):
    def get(self, request):
        groups = StudyGroup.objects.all()
        return render(request, 'study_group/study_groups.html', {'study_groups': groups})


class JoinStudyGroup(LoginRequiredMixin, View):
    def post(self, request, pk):
        group = StudyGroup.objects.get(pk=pk)
        user = request.user
        group.users.add(user)
        return redirect('room', title=group.title)
