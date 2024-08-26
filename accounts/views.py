"""
views.py
--------

This module defines the core views for the `faceid` app, which include user registration, login, 
logout, and profile management. It also handles the display of user photos and victories in the profile page.

"""

import base64
from django.shortcuts import render
from django.utils.translation import gettext as _
from django.contrib.auth.models import User
from faceid.models import UserPhoto, UserProfile


def login(request):
    """
    Handles user login and renders the login page.

    :param request: The HTTP request object.
    :return: Rendered HTML page for user login.
    """    
    return render(
        request, "accounts/login.html", {"title": _("Логін"), "page": "login", "app": "accounts"}
    )

def logout(request):
    """
    Handles user logout and renders the logout page.

    :param request: The HTTP request object.
    :return: Rendered HTML page for user logout.
    """    
    return render(
        request, "accounts/logout.html", {"title": _("Вихід"), "page": "logout", "app": "accounts"}
    )

def signup(request):
    """
    Handles user registration and renders the signup page.

    :param request: The HTTP request object.
    :return: Rendered HTML page for user signup.
    """    
    return render(
        request, "accounts/signup.html", {"title": _("Реєстрація"), "page": "signup", "app": "accounts"}
    )


def user_profile(request, username):
    """
    Retrieves and displays the user's profile page, including user photo and victories.

    :param request: The HTTP request object.
    :param username: The username of the user whose profile is being accessed.
    :return: Rendered HTML page displaying the user's profile information.
    """    
    user = User.objects.get(username=username)
    
    # Завантаження фото користувача з бази даних
    try:
        user_photo_obj = UserPhoto.objects.get(user=user)
        user_photo = base64.b64encode(user_photo_obj.photo).decode('utf-8')
    except UserPhoto.DoesNotExist:
        user_photo = None
    
    # Завантаження кількості перемог або створення профілю, якщо він не існує
    user_profile_obj, created = UserProfile.objects.get_or_create(user=user)
    victories = user_profile_obj.victories

    return render(request, 'accounts/user_profile.html', {
        'user': user,
        'user_photo': user_photo,
        'title': _("Профіль"),
        'victories': victories  # кількість перемог передається у шаблон
    })



