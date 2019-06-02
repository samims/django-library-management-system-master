from django.shortcuts import render, redirect
from django.contrib.auth import (authenticate,
                                 login,
                                 logout
                                 )
from accounts.forms import UserRegistrationForm


def register_view(request):  # Creates a New Account & login New users
    if request.user.is_authenticated:
        return redirect("/")
    else:
        title = "Register"
        form = UserRegistrationForm(request.POST or None)
        print(form.is_valid())
        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data.get("password1")
            user.set_password(password)
            user.save()
            # new_user = authenticate(email=user.email, password=password)
            login(request, user)
            return redirect("/books")

        context = {"title": title, "form": form}

        return render(request, "accounts/signup.html", context)


def login_view(request):
    if request.method == "GET":
        if request.user.is_authenticated:
            if request.user.is_staff:
                return redirect('management:requested_books')
            return redirect('/books')
        return render(request, 'accounts/login.html')

    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            return redirect("/books")
        else:
            return render(request, 'accounts/login.html', {'error_message': 'Your account has been disabled'})
    else:
        return render(request, 'accounts/login.html', {'error_message': 'Invalid login'})


def logout_view(request):
    logout(request)
    return redirect('/login')
