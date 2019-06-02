from django.contrib import admin
from .models import Book, Borrow, Student


admin.site.register(Book)
admin.site.register(Borrow)
admin.site.register(Student)
# Register your models here.
