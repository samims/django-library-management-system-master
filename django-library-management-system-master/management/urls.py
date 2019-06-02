from django.urls import path
from .views import RequestedBooks, approve, returning, students

#

app_name = 'management'
urlpatterns = [
    path('requested-books/', RequestedBooks.as_view(), name='requested_books'),
    path('approve/', approve, name='approve_book'),
    path('return/', returning, name='return_book'),
    path('students/', students, name="students"),

]
