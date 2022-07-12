from django.contrib import messages
from django.contrib.auth.models import Group
from django.shortcuts import render, redirect
from .forms import CreateUserForm, CreateLibraryForm

# Create your views here.
from django.views import View


class RegisterView(View):
    def post(self, request):
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            if request.POST.get('submit') == 'user_reg':
                group = Group.objects.get(name='User')
                user.groups.add(group)

            elif request.POST.get('submit') == 'library_reg':
                group = Group.objects.get(name='Librarian')
                user.groups.add(group)

            user.set_password(form.cleaned_data.get('password'))
            user.save()
            return redirect('homepage')
        else:
            messages.error(request, 'Cannot create account')
            return render(request, 'accounts/register.html', {'form': form})

    def get(self, request):
        form = CreateUserForm()
        context = {
            'form': form
        }
        return render(request, 'accounts/register.html', context)


class LoginView(View):
    def post(self, request):
        return render(request, 'accounts/login.html')
    def get(self, request):
        return render(request, 'accounts/login.html')

class LibraryRegisterView(View):
    def post(self, request):
        library_form = CreateLibraryForm(request.POST, request.FILES)
        if library_form.is_valid():
            library_form.save()
            return redirect('register')
        else:
            return render(request, 'accounts/library_register.html', {'library_form': library_form})

    def get(self, request):
        library_form = CreateLibraryForm()
        context = {
            'library_form': library_form
        }
        return render(request, 'accounts/library_register.html', context)
