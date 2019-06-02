from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from django.shortcuts import redirect
from library.models import Book, Borrow, Student
from django.shortcuts import get_object_or_404


# Create your views here.


class RequestedBooks(View):
    def get_queryset(self):
        qs = Borrow.objects.all()
        return qs

    def get(self, request):
        context = {
            'borrow_list': self.get_queryset()
        }

        return render(request, 'management/requested_book.html', context=context)


# class ApproveBook(View):
#     def get(self, request, pk,):
#         print(request.GET, '------------')
#         # borrow_obj = get_object_or_404(klass=Borrow, id=pk)
#         # book_obj =
#         return redirect('management:requested_books')

def approve(request):
    student_id = request.GET.get('student')
    book_id = request.GET.get('book')
    borrow_id= request.GET.get('borrow')
    # student_obj = Student.objects.get(id=student_id)
    student_obj = get_object_or_404(Student, id=student_id)
    book_obj = get_object_or_404(Book, id=book_id)
    borrow_obj = get_object_or_404(Borrow, id=borrow_id)
    # borrow

    book_obj.available -= 1
    book_obj.save()
    borrow_obj.status = 'Borrowed'
    borrow_obj.approved = True
    borrow_obj.save()
    return redirect('management:requested_books')