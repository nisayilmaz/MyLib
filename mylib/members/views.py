from django.contrib import messages
from django.contrib.auth.models import Group
from django.shortcuts import render, redirect
from .forms import CreateLibraryForm, CreateUserForm
from library.models import Library

# Create your views here.
from django.views import View


class RegisterView(View):
    def post(self, request):
        if request.POST.get('submit') == 'user_reg':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                user = form.save()
                group = Group.objects.get(name='Customer')
                user.groups.add(group)
                return redirect('homepage')
            else:
                messages.error(request, 'Failed to create account')
                return redirect('register')

        elif request.POST.get('submit') == 'library_reg':
            form = CreateLibraryForm(request.POST)
            if form.is_valid():
                user = form.save()
                group = Group.objects.get(name='Library')
                user.groups.add(group)
                new_lib = Library(name=form.cleaned_data['username'],
                                  address=form.cleaned_data['library_address'],
                                  )
                new_lib.save()
                return redirect('homepage')
            else:
                messages.error(request, 'Zort')
                return redirect('register')

    def get(self, request):

        lib_form = CreateLibraryForm()
        user_form = CreateUserForm()
        context = {
            'lib_form': lib_form,
            'user_form': user_form,
        }
        return render(request, 'members/register.html', context)
