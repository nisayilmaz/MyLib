from django.urls import path
from .views import RegisterView, LoginView, LibraryRegisterView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('library_register/', LibraryRegisterView.as_view(), name='library_register'),


]
