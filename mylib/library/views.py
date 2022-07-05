from django.shortcuts import render
from django.views import View
from .models import Library


class LibraryView(View):
    def get(self, request):
        all_libraries = Library.objects.all()
        return render(request, 'library/library.html', {'all_libraries': all_libraries})


class LibraryDetailView(View):
    def get(self, request):
        return render(request, 'library/library_detail.html')

