
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


def privacy_policy(request):
    return render(
        request,
        "home/privacy_policy.html",
        {"title": "Політика конфіденційності", "page": "privacy_policy", "app": "home"},
    )


def presentation_of_the_project(request):
    return render(
        request,
        "home/presentation_of_the_project.html",
        {
            "title": "Презентація проєкту",
            "page": "presentation_of_the_project",
            "app": "home",
        },
    )

