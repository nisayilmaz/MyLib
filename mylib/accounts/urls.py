from django.urls import path
from . import views
from .views import RegisterView, LoginView, LibraryRegisterView, LogoutView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('library_register/', LibraryRegisterView.as_view(), name='library_register'),


]
