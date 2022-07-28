from django.urls import path
from .views import LibraryView, LibraryDetailView, LibrarianDashboardView, AddBookView, BookDetailView, DeleteBookView, \
    EditBookView, BorrowBookView, ReturnBookView, AddBookFromGoogleView

urlpatterns = [
    path('', LibraryView.as_view(), name='libraries_home'),
    path('<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),
    path('dashboard', LibrarianDashboardView.as_view(), name='dashboard'),
    path('add_book', AddBookView.as_view(), name='add_book'),
    path('books/<int:pk>', BookDetailView.as_view(), name='book_detail'),
    path('books/<int:pk>/delete_book', DeleteBookView.as_view(), name='delete_book'),
    path('books/<int:pk>/borrow_book', BorrowBookView.as_view(), name='borrow_book'),
    path('books/<int:pk>/return_book', ReturnBookView.as_view(), name='return_book'),
    path('books/<int:pk>/edit_book', EditBookView.as_view(), name='edit_book'),
    path('lib/add_book/<int:index>', AddBookFromGoogleView.as_view(), name='add'),
]
