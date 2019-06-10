from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.shortcuts import render
from django.views import View

from library.models import Book, Borrow, Student


# Create your views here.


class RequestedBooks(LoginRequiredMixin, View):
    def get(self, request):
        if not request.user.is_staff:
            return redirect('/books')
        requested_list = Borrow.objects.filter(status='Requested')
        borrowed_list = Borrow.objects.filter(status='Borrowed')
        return render(request, 'management/backup.html',
                      context={'requested_list': requested_list, 'borrowed_list': borrowed_list})


@login_required(login_url='/login')
def approve(request):
    if not request.user.is_staff:
        return redirect('/books')
    student_id = request.GET.get('student')
    book_id = request.GET.get('book')
    borrow_id = request.GET.get('borrow')
    # student_obj = Student.objects.get(id=student_id)
    student_obj = get_object_or_404(Student, id=student_id)
    book_obj = get_object_or_404(Book, id=book_id)
    borrow_obj = get_object_or_404(Borrow, id=borrow_id)
    book_obj.available -= 1
    book_obj.save()
    borrow_obj.status = 'Borrowed'
    borrow_obj.approved = True
    borrow_obj.save()
    return redirect('management:requested_books')


def reject(request):
    if not request.user.is_staff:
        return redirect('/books')
    # student_id = int(request.GET.get('student'))
    book_id = int(request.GET.get('book'))
    borrow_id = int(request.GET.get('borrow'))
    borrow_obj = get_object_or_404(Borrow, id=borrow_id)
    # student_obj = get_object_or_404(Student, id=student_id)
    book_obj = get_object_or_404(Book, id=book_id)
    borrow_obj.book.remove(book_obj)
    return redirect('management:requested_books')


def returning(request):
    b_id = int(request.GET.get("borrow_id"))
    borrow = get_object_or_404(Borrow, id=b_id)
    borrow.date = datetime.now()
    borrow.status = "Returned"
    borrow.save()
    return redirect('management:requested_books')


@login_required(login_url='/login')
def students(request):
    if not request.user.is_staff:
        return redirect('/books')
    if request.method == "POST":
        sid = request.POST["sid"]
        firstname = request.POST["firstname"]
        lastname = request.POST["lastname"]
        department = request.POST["department"]
        section = request.POST["section"]
        year = request.POST["year"]

        student = Student(student_id=sid, firstname=firstname, lastname=lastname, department=department,
                          section=section, year=year)
        student.save()
        return redirect("/students")
    students = Student.objects.all()
    return render(request, "students.html", {"students": students})
