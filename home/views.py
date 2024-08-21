from django.utils.translation import gettext as _
from django.shortcuts import render
from django.shortcuts import redirect
from django.utils import translation


# Create your views here.
def index(request):
    return render(
        request, "home/index.html", {"title": _("Головна"), "page": "index", "app": "home"}
    )


def cognition(request):
    return render(
        request,
        "home/cognition.html",
        {"title": _("Пізнання"), "page": "cognition", "app": "home"},
    )


def team(request):
    return render(
        request, "home/team.html", {"title": _("Команда"), "page": "team", "app": "home"}
    )


def privacy_policy(request):
    return render(
        request,
        "home/privacy_policy.html",
        {"title": _("Політика конфіденційності"), "page": "privacy_policy", "app": "home"},
    )


def presentation_of_the_project(request):
    return render(
        request,
        "home/presentation_of_the_project.html",
        {
            "title": _("Презентація проєкту"),
            "page": "presentation_of_the_project",
            "app": "home",
        },
    )


def set_language(request):
    user_language = request.POST.get('language')
    
    if user_language:
        translation.activate(user_language)
        request.session['django_language'] = user_language
        request.session.modified = True
    
    return redirect(request.POST.get('next', '/'))


