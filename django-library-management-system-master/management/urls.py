from django.urls import path
from .views import RequestedBooks, approve

#

app_name = 'management'
urlpatterns = [
    path('requested-books/', RequestedBooks.as_view(), name='requested_books'),
    # path('approve/<int:pk>/', ApproveBook.as_view(), name='approve_book')
    path('approve/', approve, name='approve_book')
]
