from datetime import datetime
import os
import openpyxl
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, Http404, HttpResponse
from django.shortcuts import render, redirect
from django.views.generic.list import ListView

# Create your views here.
from library.models import Book, Category, Student, Borrow


class BookListView(LoginRequiredMixin, ListView):
    model = Book
    queryset = Book.objects.filter(available__gte=1)
    template_name = 'library/client.html'

    def get_context_data(self, *args, **kwargs):
        obj_list = Borrow.objects.filter(student__id=self.request.user.student.id)
        context = super(BookListView, self).get_context_data(*args, **kwargs)
        borrowed_list = list()
        requested_list = list()
        for obj in obj_list.filter(status='Borrowed'):
            borrowed_book_list = list(obj.book.values_list('id', flat=True))
            borrowed_list.extend(borrowed_book_list)

        for obj in obj_list.filter(status='Requested'):
            requested_book_list = list(obj.book.values_list('id', flat=True))
            requested_list.extend(requested_book_list)

        context['borrowed_list'] = borrowed_list
        print(borrowed_list)
        context['requested_list'] = requested_list
        return context


@login_required(login_url='/login')
def borrow(request):
    book_queryset = Book.objects.filter(available__gte=1)
    user_id = request.GET.get('user_id')
    book = request.GET.get('book_id')

    try:
        student_obj = Student.objects.get(user=request.user)
    except Student.DoesNotExist:
        raise Http404("Student of id {} does not exist".format(request.user.id))
    try:
        # print("---------------", book, type(book))
        book_obj = Book.objects.get(id=int(book))

    except Book.DoesNotExist:
        raise Http404("Book Does not exist")

    status = "Requested"
    if Borrow.objects.filter(book__id=book, student__id=request.user.id):
        return redirect('/books')
    b = Borrow(qty=1, status=status)
    # print(b, "b")
    b.save()
    b.student.add(student_obj)
    b.book.add(book_obj)
    return redirect("/books/")


def index(request):
    return render(request, "index.html", {})


def categories(request):
    if request.method == "POST":
        title = request.POST['title']

        Category(title=title).save()
        return redirect('/categories')
    categories = Category.objects.all()
    return render(request, "category.html", {"categories": categories})


def delete_category(request, id):
    category = Category.objects.filter(id=id)
    category.delete()
    return redirect('/categories')


def edit_category(request, id):
    category = Category.objects.filter(id=id).get()
    return JsonResponse({'title': category.title})


def books(request):
    if request.method == "POST":
        title = request.POST['title']
        author = request.POST['author']
        cat = Category.objects.get(id=int(request.POST['category_id']))
        description = request.POST['description']
        available = int(request.POST['quantity'])

        book = Book(title=title, author=author, description=description, available=available)
        book.save()
        if book.categories.add(cat):
            return redirect('/books')
    books = Book.objects.all()
    categories = Category.objects.all()
    return render(request, "books.html", {"books": books, "categories": categories})


def edit_book(request, id):
    book = Book.objects.filter(id=id).get()
    return JsonResponse(
        {'title': book.title, 'author': book.author, 'description': book.description, 'available': book.available})


def delete_book(request, id):
    book = Book.objects.filter(id=id).get()
    book.delete()
    return redirect("/books")


# def borrow(request):
#     if request.method == "POST":
#         student_id = request.POST['student_id']
#         student = Student.objects.get(id=student_id)
#         # status = "Borrowed"
#         status = "Requested"
#         books_id = request.POST.getlist('selector')
#         for book_id in books_id:
#             book = Book.objects.get(id=book_id)
#             if Borrow.objects.filter(book__id=book_id):
#                 return redirect('/borrow')
#             b = Borrow(qty=1, status=status)
#             b.save()
#             b.student.add(student)
#             b.book.add(book)
#             return redirect("/borrow")
#     students = Student.objects.all()
#     books = Book.objects.all()
#     datas = []
#     for book in books:
#         left = Borrow.objects.filter(status="Borrowed", book__title=book.title).aggregate(Sum('qty'))
#         if left['qty__sum'] is None:
#             l = 0
#         else:
#             l = int(left['qty__sum'])
#         datas.append(book.available - l)
#     return render(request, "borrow.html", {"datas": zip(books, datas), "students": students})


def returning(request):
    if request.method == "POST":
        b_id = int(request.POST["borrow_id"])
        borrow = Borrow.objects.get(id=b_id)
        borrow.date = datetime.now()
        borrow.status = "Returned"
        borrow.save()
        return redirect('/returning')
    borrows = Borrow.objects.all()
    return render(request, "return.html", {"borrows": borrows})


def students(request):
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


def upload_books(request):
    cwd = os.getcwd()
    myfile = os.path.join(cwd, "book.XLSX")
    wb = openpyxl.load_workbook(myfile)
    for sheet in wb.get_sheet_names():
        cur_sheet = wb.get_sheet_by_name(sheet)
        for cell in cur_sheet.values:
            print(cell)
            book = Book.objects.create(title=cell[2], author=cell[3], year=cell[5], price=cell[6])
            category = cell[4]

            if category:
                if not Category.objects.filter(title=cell[4]):
                    category = Category.objects.create(title=category)
                else:
                    category = Category.objects.filter(title=category).first()
                book.categories.add(category)
    return HttpResponse("Hi")