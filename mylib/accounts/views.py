from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group
from django.shortcuts import render, redirect
from .forms import CreateUserForm, CreateLibraryForm, LoginForm

# Create your views here.
from django.views import View


class RegisterView(View):
    def post(self, request):
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()

            if request.POST.get('submit') == 'library_reg':
                group = Group.objects.get(name='Librarian')
                user.groups.add(group)
            if request.POST.get('submit') == 'user_reg':
                group = Group.objects.get(name='User')
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


class LoginView(View):
    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data.get('username')
            password = login_form.cleaned_data.get('password')
            user = authenticate(request, username= username, password= password)
            if user is not None:
                login(request, user)
                return redirect('homepage')
            else:
                return redirect('login')

        return redirect('login')

    def get(self, request):
        login_form = LoginForm()
        return render(request, 'accounts/login.html', {'login_form': login_form})


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('homepage')