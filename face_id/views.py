import face_recognition
import cv2
import numpy as np
from django.shortcuts import render, redirect
from django.http import JsonResponse
from .forms import RegisterForm
from django.contrib.auth import login, logout
from .models import CustomUser


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password"])

            if request.FILES.get("image"):
                image_file = request.FILES["image"]
                np_img = np.frombuffer(image_file.read(), np.uint8)
                img = cv2.imdecode(np_img, cv2.IMREAD_COLOR)

                # Знайти обличчя за допомогою face_recognition
                face_locations = face_recognition.face_locations(img)

                if face_locations:
                    # Обчислити вектори обличчя
                    face_encodings = face_recognition.face_encodings(
                        img, face_locations
                    )

                    if face_encodings:
                        face_vector = face_encodings[0]
                        user.save_face_vector(face_vector)

            user.save()
            return redirect("/")
        else:
            print(form.errors)

    else:
        form = RegisterForm()
    return render(request, "face_id/register.html", {"form": form})


def face_login(request):
    if request.method == "POST" and request.FILES.get("image"):
        file = request.FILES["image"]
        np_img = np.frombuffer(file.read(), np.uint8)
        img = cv2.imdecode(np_img, cv2.IMREAD_COLOR)

        # Використовуємо face_recognition для розпізнавання обличчя
        face_encodings = face_recognition.face_encodings(img)

        if face_encodings:
            input_face_vector = face_encodings[0]

            # Порівняння векторів облич з базою даних
            for user in CustomUser.objects.all():
                try:
                    db_face_vector = np.frombuffer(user.face_vector, dtype=np.float64)

                    if len(db_face_vector) == len(
                        input_face_vector
                    ):  # Додаткова перевірка на розмір вектора
                        match_results = face_recognition.compare_faces(
                            [db_face_vector], input_face_vector
                        )

                        if match_results[0]:
                            login(request, user)
                            return JsonResponse({"success": True, "redirect_url": "/"})
                except Exception as e:
                    print(f"Error comparing face vector: {e}")

        return JsonResponse({"success": False})

    return render(request, "face_id/face_login.html")


def logout_view(request):
    logout(request)  # Виконує вихід користувача
    return redirect(
        "/"
    )  # Перенаправляє користувача на головну сторінку або іншу сторінку після виходу
