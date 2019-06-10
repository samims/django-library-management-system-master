from django.contrib import admin
from .models import Book, Borrow, Student, Category


admin.site.register((Book, Borrow, Student, Category))
# admin.site.register(Borrow)
# admin.site.register(Student)
# # Register your models here.
