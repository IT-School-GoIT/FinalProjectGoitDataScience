from django.shortcuts import render

# Create your views here.


def login(request):
    return render(
        request, "accounts/login.html", {"title": "Логін", "page": "login", "app": "accounts"}
    )

def logout(request):
    return render(
        request, "accounts/logout.html", {"title": "Логін", "page": "logout", "app": "accounts"}
    )

def signup(request):
    return render(
        request, "accounts/signup.html", {"title": "Логін", "page": "signup", "app": "accounts"}
    )