import io
import face_recognition
from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import UserPhoto
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import logout, login as auth_login
from django.contrib.auth.models import User

from django.contrib.sessions.models import Session

# Видалено дублювання імпорту 'UserPhoto' і 'auth_login'


def index(request):
    return render(request, "accounts/signup.html")


@csrf_exempt
def register(request):
    if request.method == "POST":
        name = request.POST.get("name")
        photo = request.FILES.get("photo")

        if name and photo:
            # Створюємо нового користувача в Django
            user = User.objects.create_user(
                username=name, password="temporary_password"
            )

            # Зберігаємо фото користувача
            photo_content = photo.read()
            user_photo = UserPhoto(user=user, photo=photo_content)
            user_photo.save()

            # Автоматичний вхід користувача після реєстрації
            auth_login(request, user)

            return JsonResponse({"success": True, "name": name})

    return JsonResponse({"success": False})


@csrf_exempt
def login(request):
    if request.method == "POST":
        photo = request.FILES.get("photo")

        if photo:
            login_image_content = photo.read()
            login_image = face_recognition.load_image_file(
                io.BytesIO(login_image_content)
            )
            login_face_encodings = face_recognition.face_encodings(login_image)

            if not login_face_encodings:
                return JsonResponse({"success": False})

            users = UserPhoto.objects.all()
            for user_photo in users:
                registered_image_content = user_photo.photo

                try:
                    registered_image = face_recognition.load_image_file(
                        io.BytesIO(registered_image_content)
                    )
                    registered_face_encodings = face_recognition.face_encodings(
                        registered_image
                    )

                    if (
                        len(registered_face_encodings) > 0
                        and face_recognition.compare_faces(
                            registered_face_encodings, login_face_encodings[0]
                        )[0]
                    ):
                        # Якщо обличчя співпадає, автоматично виконуємо вхід
                        user = user_photo.user
                        auth_login(request, user)
                        return JsonResponse({"success": True, "name": user.username})
                except Exception as e:
                    print(f"Error processing image: {e}")
                    continue

    return JsonResponse({"success": False})


def success(request):
    user_name = request.GET.get("user_name")
    return redirect("game2:play_game")


def user_logout(request):
    logout(request)
    Session.objects.filter(session_key=request.session.session_key).delete()
    return redirect('home:index')
