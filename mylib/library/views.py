import datetime
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .models import Library, Book, Borrowed
from .forms import BookForm
from .mixins import LibrarianPermissionRequiredMixin


class LibraryView(LoginRequiredMixin, View):
    def get(self, request):
        all_libraries = Library.objects.all()
        return render(request, 'library/library.html', {'all_libraries': all_libraries})


class LibraryDetailView(LoginRequiredMixin, View):
    def get(self, request, pk):
        library = Library.objects.get(pk=pk)
        books = Book.objects.filter(location=pk)
        return render(request, 'library/library_detail.html', {'library': library, 'books': books, })


class BookDetailView(LoginRequiredMixin, View):
    def get(self, request, pk):
        book = get_object_or_404(Book, pk=pk)
        try:
            borrowed_book = Borrowed.objects.get(returned__isnull=True, book=book.id)
        except Borrowed.DoesNotExist:
            borrowed_book = None
        library = book.location
        edit_form = BookForm(instance=book)
        return render(request, 'library/book_detail.html',
                      {'book': book, 'library': library, 'edit_form': edit_form, 'borrowed_book': borrowed_book})


class LibrarianDashboardView(LibrarianPermissionRequiredMixin, View):
    def get(self, request):
        pk = request.user.library.id
        library = Library.objects.get(pk=pk)
        borrowed_books = Borrowed.objects.filter(book__location=library)
        not_returned = borrowed_books.filter(returned=None)
        books = Book.objects.filter(location=pk)
        form = BookForm()
        return render(request, 'library/dashboard.html',
                      {'library': library, 'books': books, 'form': form, 'borrowed_books': borrowed_books, 'lent': not_returned})


class AddBookView(LibrarianPermissionRequiredMixin, View):
    def post(self, request):
        book_form = BookForm(request.POST, request.FILES)
        if book_form.is_valid():
            if 'confirm' in request.POST:
                new_book = Book(**book_form.cleaned_data, location=request.user.library)
                new_book.save()
            return redirect('dashboard')
        else:
            return render(request, 'library/dashboard.html', {'book_form': book_form})


class DeleteBookView(LibrarianPermissionRequiredMixin, View):
    def post(self, request, pk):
        book = get_object_or_404(Book, pk=pk)
        if 'confirm' in request.POST:
            book.delete()
            return redirect('dashboard')
        return redirect('book_detail')

    def get(self, request, pk):
        book = get_object_or_404(Book, pk=pk)
        return render(request, 'library/delete_book.html', {'book': book})


class EditBookView(LibrarianPermissionRequiredMixin, View):
    def post(self, request, pk):
        book = Book.objects.get(pk=pk)
        book_form = BookForm(request.POST, request.FILES, instance=book)
        if book_form.is_valid():
            if 'confirm' in request.POST:
                book.save()
            return redirect('book_detail', pk=pk)
        else:
            messages.error(request, 'Unable to edit book.')
            return redirect('book_detail', pk=pk)


class BorrowBookView(View):
    def post(self, request, pk):
        user = request.user
        book = Book.objects.get(pk=pk)
        borrow_date = datetime.date.today()
        return_date = borrow_date + datetime.timedelta(days=15)
        borrowed_book = Borrowed(borrowed_by=user, book=book, borrow_date=borrow_date,
                                 latest_return_date=return_date)
        book_count = Borrowed.objects.filter(borrowed_by=user, returned__isnull=True).count()

        if 'confirm_borrow' in request.POST:
            if book_count < 3 and book.available:
                borrowed_book.save()
                messages.success(request, 'Book borrowed')
                book.available = False
                book.save()
                return redirect('book_detail', pk=pk)

        messages.error(request, 'Unable to borrow book.')
        return redirect('book_detail', pk=pk)


class ReturnBookView(View):
    def post(self, request, pk):
        user = request.user
        book = Book.objects.get(pk=pk)
        return_date = datetime.date.today()
        is_book_borrowed = Borrowed.objects.filter(borrowed_by=user, returned__isnull=True, book=book).exists()
        if 'confirm_return' in request.POST:
            if is_book_borrowed:
                borrowed_book = Borrowed.objects.get(borrowed_by=user, returned__isnull=True, book=book)
                borrowed_book.returned = return_date
                book.available = True
                borrowed_book.save()
                book.save()
                messages.success(request, 'Book returned')
                return redirect('book_detail', pk=pk)

        messages.error(request, 'Unable to return book.')
        return redirect('book_detail', pk=pk)
