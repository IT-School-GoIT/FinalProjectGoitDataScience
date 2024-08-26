"""
views.py
--------

This module defines views for user registration, login, and image resizing functionality using face recognition. 
It also handles the logic for user session management, including automatic login after registration 
and facial recognition-based login.

"""

import io
import face_recognition
from PIL import Image
from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import UserPhoto
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import logout, login as auth_login
from django.contrib.auth.models import User

from django.contrib.sessions.models import Session

# Видалено дублювання імпорту 'UserPhoto' і 'auth_login'


def index(request):
    """
    Renders the signup page.
    
    :param request: The HTTP request object.

    :return HttpResponse: Rendered signup page.
    """    
    return render(request, "accounts/signup.html")


def resize_image(image_content, size=(400, 300)):
    """
    Resizes the uploaded image to the specified dimensions.

    :param image_content: (bytes): The image content in bytes.
    :param size: (tuple): Desired dimensions (width, height).

    :return bytes: Resized image content in JPEG format.
    """    
    image = Image.open(io.BytesIO(image_content))

    # Перевірка на альфа-канал і перетворення в RGB, якщо необхідно
    if image.mode == 'RGBA':
        image = image.convert('RGB')

    resized_image = image.resize(size)
    byte_arr = io.BytesIO()
    resized_image.save(byte_arr, format='JPEG')
    return byte_arr.getvalue()

@csrf_exempt
def register(request):
    """
    Handles user registration, image upload, and auto-login.

    :param request: The HTTP request object.

    :return JsonResponse: Success or failure status of the registration process.
    """    
    if request.method == "POST":
        name = request.POST.get("name")
        photo = request.FILES.get("photo")

        if name and photo:
            # Нормалізація розміру фото
            photo_content = photo.read()
            resized_photo_content = resize_image(photo_content)

            # Створюємо нового користувача
            user = User.objects.create_user(username=name, password="temporary_password")

            # Зберігаємо фото користувача
            user_photo = UserPhoto(user=user, photo=resized_photo_content)
            user_photo.save()

            # Автоматичний вхід користувача після реєстрації
            auth_login(request, user)

            return JsonResponse({"success": True, "name": name})

    return JsonResponse({"success": False})


@csrf_exempt
def login(request):
    """
    Handles user login through face recognition.

    :param request: The HTTP request object.

    :return JsonResponse: Success or failure status of the login process.
    """    
    if request.method == "POST":
        photo = request.FILES.get("photo")

        if photo:
            login_image_content = resize_image(photo.read())
            login_image = face_recognition.load_image_file(io.BytesIO(login_image_content))
            login_face_encodings = face_recognition.face_encodings(login_image)

            if not login_face_encodings:
                return JsonResponse({"success": False})

            users = UserPhoto.objects.all()
            for user_photo in users:
                registered_image_content = user_photo.photo

                try:
                    registered_image = face_recognition.load_image_file(io.BytesIO(registered_image_content))
                    registered_face_encodings = face_recognition.face_encodings(registered_image)

                    if len(registered_face_encodings) > 0 and face_recognition.compare_faces(registered_face_encodings, login_face_encodings[0])[0]:
                        # Вхід у систему
                        user = user_photo.user
                        auth_login(request, user)
                        return JsonResponse({"success": True, "name": user.username})
                except Exception as e:
                    print(f"Error processing image: {e}")
                    continue

    return JsonResponse({"success": False})


def success(request):
    """
    Redirects the user to the game after successful login.

    :param request: The HTTP request object.

    :return HttpResponse: Redirect to the game page.
    """    
    user_name = request.GET.get("user_name")
    return redirect("game2:play_game")


def user_logout(request):
    """
    Logs out the user and deletes their session.

    :param request: The HTTP request object.

    :return HttpResponse: Redirects to the home page.
    """    
    logout(request)
    Session.objects.filter(session_key=request.session.session_key).delete()
    return redirect('home:index')
