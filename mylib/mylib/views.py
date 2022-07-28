from django.contrib import messages
from django.contrib.postgres.search import SearchVector
from django.shortcuts import render, redirect
from django.views import View
from library.models import Book
import requests


class HomepageView(View):
    def get(self, request):
        return render(request, 'mylib/index.html')


class SearchView(View):
    def post(self, request):
        searched = request.POST['searched']
        s = searched + '&maxResults=40'
        key = '&key=AIzaSyDfBudLFvhRiH6fpR9dI4AxssqJH2Zwmto'
        url = 'https://www.googleapis.com/books/v1/volumes?q=' + s + key
        response = requests.get(url)
        data = response.json()
        try:
            book = data['items']
            request.session['book_data'] = book
        except:
            book = None
            messages.error(request, 'No results')
        if not len(str(searched).strip()) == 0:
            found = Book.objects.annotate(search=SearchVector("title", "author", "isbn")).filter(
                search=searched)
            return render(request, 'mylib/search_results.html', {'searched': searched, 'found': found, 'books':book})
        else:
            messages.error(request, 'Search bar is empty, please type to search.')
            return redirect('search')

    def get(self, request):
        return render(request, 'mylib/search_results.html')
