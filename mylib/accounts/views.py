from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Group
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.mail import EmailMessage
from .mixins import UnauthenticatedRequiredMixin
from .forms import CreateUserForm, CreateLibraryForm, LoginForm, ResetPasswordForm, EditProfileForm
from django.views import View
from django.contrib.sites.shortcuts import get_current_site
from .token import account_activation_token
from .models import User, Profile, FriendRequest
from django.contrib.auth.forms import SetPasswordForm
from library.models import Borrowed


class RegisterView(UnauthenticatedRequiredMixin, View):
    def post(self, request):
        form = CreateUserForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate your MyLib account!'
            message = render_to_string('acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()

            if request.POST.get('submit') == 'library_reg':
                group = Group.objects.get(name='Librarian')
                user.groups.add(group)
            if request.POST.get('submit') == 'user_reg':
                group = Group.objects.get(name='User')
                user.groups.add(group)
            user.set_password(form.cleaned_data.get('password'))
            user.save()
            messages.info(request, 'Check your mailbox to activate your account.')
            return redirect('login')
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


class LoginView(UnauthenticatedRequiredMixin, View):
    def post(self, request):
        login_form = LoginForm(request.POST)
        if 'login' in request.POST:
            if login_form.is_valid():
                username = login_form.cleaned_data.get('username')
                password = login_form.cleaned_data.get('password')
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('homepage')
                else:
                    messages.error(request, 'Username or password not correct')
                    return redirect('login')
        return redirect('login')

    def get(self, request):
        form = ResetPasswordForm()
        login_form = LoginForm()
        return render(request, 'accounts/login.html', {'login_form': login_form, 'form': form})


class LogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        return redirect('homepage')


class ActivateView(View):
    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, user.DoesNotExist):
            user = None
        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            profile = Profile(user=user)
            profile.save()
            messages.success(request, 'Your account is activated!')
            return redirect('login')
        else:
            messages.error(request, 'Activation is invalid!')
            return redirect('register')


class ResetPasswordSubmitView(View):
    def post(self, request):
        current_site = get_current_site(request)
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            user = get_object_or_404(User, username=username)
            mail_subject = 'Reset your password.'
            message = render_to_string('reset_password_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = user.email
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()
            messages.info(request, 'Password reset link has been sent to your email.')
        return redirect('login')


class ResetPasswordView(View):
    def post(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, user.DoesNotExist):
            user = None
        if user is not None and account_activation_token.check_token(user, token):
            form = SetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Your password was successfully updated!')
                return redirect('login')
            else:
                messages.error(request, 'Please correct the error below.')
                return redirect('reset_password', uidb64=uidb64, token=token)
        messages.error(request, 'Cannot reset password, please try again.')
        return redirect('login')

    def get(self, request, uidb64, token):
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
        form = SetPasswordForm(user)
        return render(request, 'accounts/reset_password.html', {'form': form})


class ProfileView(LoginRequiredMixin, View):
    def get(self, request, pk):
        user = User.objects.get(pk=pk)
        profile = get_object_or_404(Profile, user=user)
        books = Borrowed.objects.filter(borrowed_by=user).distinct('book')
        friend_requests = FriendRequest.objects.filter(to_user=user)
        friends = user.friends.all()
        friends_with = False
        form = EditProfileForm(instance=user)
        if request.user != user:
            friends_with = user.friends.filter(pk=request.user.id).exists()
        return render(request, 'accounts/profile.html',
                      {'profile': profile, 'books': books, 'friend_requests': friend_requests, 'friends': friends,
                       'friends_with': friends_with, 'form': form})


class SendFriendRequest(LoginRequiredMixin, View):
    def post(self, request):
        pk = request.POST.get('to_id')
        to_user = get_object_or_404(User, pk=pk)
        if request.user != to_user:
            try:
                req = FriendRequest.objects.get(to_user=to_user, from_user=request.user)
                return JsonResponse({'status': 'Already sent!'})
            except FriendRequest.DoesNotExist:
                req = FriendRequest(to_user=to_user, from_user=request.user)
                req.save()
        return JsonResponse({'status': 'Friend request sent!'})


class AcceptFriendRequest(LoginRequiredMixin, View):
    def post(self, request):
        pk = request.POST.get('pk')
        req = FriendRequest.objects.get(pk=pk)
        if req.to_user == request.user:
            req.to_user.friends.add(req.from_user)
            req.from_user.friends.add(req.to_user)
            req.delete()
        return JsonResponse({'status': 'Friend added!'})


class RejectFriendRequest(LoginRequiredMixin, View):
    def post(self, request):
        pk = request.POST.get('pk')
        req = FriendRequest.objects.get(pk=pk)
        if req.to_user == request.user:
            req.delete()
        return JsonResponse({'status': 'Friend request rejected!'})


class EditProfileView(LoginRequiredMixin, View):
    def post(self, request):
        user = request.user
        profile = Profile.objects.get(user=user)
        form = EditProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            if 'confirm' in request.POST:
                profile.bio = form.cleaned_data['bio']
                if form.cleaned_data['bio'] != "" and form.cleaned_data['bio'] is not None:
                    profile.save()
                form.fields.pop('bio')
                user.save()
            return redirect('profile', pk=user.id)
        else:
            messages.error(request, 'Unable to edit profile.')
            return redirect('profile', pk=user.id)
