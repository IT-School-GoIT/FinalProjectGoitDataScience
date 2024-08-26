"""
views.py
--------

This module contains the view functions for rendering various pages and handling
language settings for the web application.

Functions:
----------

- `index(request)`:
    Renders the home page of the application.

- `cognition(request)`:
    Renders the cognition page of the application.

- `team(request)`:
    Renders the team page of the application.

- `privacy_policy(request)`:
    Renders the privacy policy page of the application.

- `documentation(request)`:
    Renders the documentation page of the application.

- `presentation_of_the_project(request)`:
    Renders the project presentation page of the application.

- `set_language(request)`:
    Sets the preferred language for the user session and updates the session to remember the language.

"""

from django.utils.translation import gettext as _
from django.shortcuts import render, redirect
from django.utils import translation


# Create your views here.
def index(request):
    """
    Render the index (home) page of the application.
    
    :param request: HttpRequest object.
    :return: Rendered template for the home page.
    """
    return render(
        request, "home/index.html", {"title": _("Головна"), "page": "index", "app": "home"}
    )


def cognition(request):
    """
    Render the cognition page of the application.
    
    :param request: HttpRequest object.
    :return: Rendered template for the cognition page.
    """
    return render(
        request,
        "home/cognition.html",
        {"title": _("Пізнання"), "page": "cognition", "app": "home"},
    )


def team(request):
    """
    Render the team page of the application.
    
    :param request: HttpRequest object.
    :return: Rendered template for the team page.
    """
    return render(
        request, "home/team.html", {"title": _("Команда"), "page": "team", "app": "home"}
    )


def privacy_policy(request):
    """
    Render the privacy policy page of the application.
    
    :param request: HttpRequest object.
    :return: Rendered template for the privacy policy page.
    """
    return render(
        request,
        "home/privacy_policy.html",
        {"title": _("Політика конфіденційності"), "page": "privacy_policy", "app": "home"},
    )


def documentation(request):
    """
    Render the documentation page of the application.

    :param request: HttpRequest object.
    :return: Rendered template for the documentation page.
    """
    return render(
        request,
        "home/documentation.html",
        {"title": _("Documentation"), "page": "documentation", "app": "home"},
    )


def presentation_of_the_project(request):
    """
    Render the project presentation page of the application.
    
    :param request: HttpRequest object.
    :return: Rendered template for the project presentation page.
    """
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
    """
    Set the preferred language for the user session.
    
    This function allows users to change the display language of the site. 
    It retrieves the language from the request, activates the language, 
    and updates the session to remember the selected language.
    
    :param request: HttpRequest object.
    :return: Redirects the user back to the previous page or the home page.
    """
    user_language = request.POST.get('language')

    if user_language:
        translation.activate(user_language)
        request.session['django_language'] = user_language
        request.session.modified = True

    return redirect(request.POST.get('next', '/'))
