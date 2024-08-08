from django.shortcuts import render


# Create your views here.
def index(request):
    return render(
        request, "home/index.html", {"title": "Головна", "page": "index", "app": "home"}
    )


def cognition(request):
    return render(
        request,
        "home/cognition.html",
        {"title": "Пізнання", "page": "cognition", "app": "home"},
    )


def team(request):
    return render(
        request, "home/team.html", {"title": "Команда", "page": "team", "app": "home"}
    )
