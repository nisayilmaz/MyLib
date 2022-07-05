from django.urls import path
from .views import LibraryView, LibraryDetailView

urlpatterns = [
    path('', LibraryView.as_view(), name='libraries_home'),
    path('detail', LibraryDetailView.as_view(), name='library_detail')
]
