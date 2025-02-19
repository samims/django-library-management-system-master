from django.conf.urls import url, include
from django.urls import path
from . import views


app_name = 'library'

urlpatterns = [
    # url(r'^index$', views.index),
    # url(r'^books$', views.books, name="books"),
    url(r'^categories$', views.categories, name="categories"),
    url(r'^returning$', views.returning, name="returning"),
    url(r'^borrow/$', views.borrow, name="borrow"),
    # url(r'^edit_book/(\d+)/$', views.edit_book, name="edit_book"),
    # url(r'^edit_category/(\d+)/$', views.edit_category, name="edit_category"),
    # url(r'^delete_book/(\d+)/$', views.delete_book, name="delete_book"),
    # url(r'^delete_category/(\d+)/$', views.delete_category, name="delete_category"),
    # path('students/', views.students, name="students"),
    path('books/', views.BookListView.as_view(), name="books"),
    path('upload/books/', views.upload_books, name='upload_books'),


]
