from django.urls import path
from .views import RegisterView, LoginView, LibraryRegisterView, LogoutView, ActivateView, ResetPasswordSubmitView, \
    ResetPasswordView, ProfileView, SendFriendRequest, AcceptFriendRequest, RejectFriendRequest, EditProfileView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/<int:pk>', ProfileView.as_view(), name='profile'),
    path('edit_profile', EditProfileView.as_view(), name='edit_profile'),
    path('add_friend/', SendFriendRequest.as_view(), name='add_friend'),
    path('accept_friend_request', AcceptFriendRequest.as_view(), name='add_friend_accept'),
    path('reject_friend_request', RejectFriendRequest.as_view(), name='reject_friend_request'),
    path('library_register/', LibraryRegisterView.as_view(), name='library_register'),
    path('activate/<uidb64>/<token>',
         ActivateView.as_view(), name='activate'),
    path('reset_password/', ResetPasswordSubmitView.as_view(), name='password_reset_submit'),
    path('reset_password/<uidb64>/<token>',
         ResetPasswordView.as_view(), name='reset_password')
]
