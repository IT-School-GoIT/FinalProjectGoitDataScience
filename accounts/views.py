import base64
from django.shortcuts import render, get_object_or_404
from django.utils.translation import gettext as _
from django.contrib.auth.models import User
from faceid.models import UserPhoto, UserProfile

# Create your views here.


def login(request):
    return render(
        request, "accounts/login.html", {"title": _("Логін"), "page": "login", "app": "accounts"}
    )

def logout(request):
    return render(
        request, "accounts/logout.html", {"title": _("Вихід"), "page": "logout", "app": "accounts"}
    )

def signup(request):
    return render(
        request, "accounts/signup.html", {"title": _("Реєстрація"), "page": "signup", "app": "accounts"}
    )


def user_profile(request, username):
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



