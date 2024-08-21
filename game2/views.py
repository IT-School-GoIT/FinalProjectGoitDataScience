from django.utils.translation import gettext as _
import os
from django.contrib.auth.models import User
from faceid.models import UserProfile

# Вимкнення GPU
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

from tensorflow.keras.models import load_model

from django.shortcuts import render, redirect
from .models import ImageForGame
import random
import numpy as np
from PIL import Image

# Завантаження попередньо навченого CIFAR-10 моделі
model = load_model("game2/cifar10_model.keras")

# Список класів CIFAR-10, що буде використовуватись для класифікації зображень
CLASSES = [
    "plane",
    "car",
    "bird",
    "cat",
    "deer",
    "dog",
    "frog",
    "horse",
    "ship",
    "truck",
]


def play_game(request):
    """
    Основна функція для гри.
    Вона відповідає за вибір випадкового зображення, обробку прогнозів моделі,
    порівняння результатів з відповіддю користувача та оновлення рахунку.
    """

    # Ініціалізація рахунку для користувача та моделі, якщо їх ще немає у сесії
    if "user_score" not in request.session:
        request.session["user_score"] = 0
    if "model_score" not in request.session:
        request.session["model_score"] = 0

    # Перевірка, чи хтось вже набрав 7 балів
    if request.session["user_score"] >= 7 or request.session["model_score"] >= 7:
        winner = _("Користувач") if request.session["user_score"] >= 7 else _("Модель cifar10.keras")

        # Якщо користувач виграв і він авторизований, оновлюємо кількість перемог у UserProfile
        if request.session["user_score"] >= 7 and request.user.is_authenticated:
            user_profile, created = UserProfile.objects.get_or_create(user=request.user)
            user_profile.victories += 1
            user_profile.save()

        return render(request, "game2/game_over.html", {"winner": winner, "title": _("Гра завершена")})

    # Вибір випадкового зображення для гри, якщо ще не було вибрано
    if "current_image_id" not in request.session:
        images = ImageForGame.objects.all()  # Отримуємо всі зображення з бази даних
        if not images.exists():
            return render(request, "game2/no_images.html")  # Якщо зображень немає
        random_image = random.choice(images)
        request.session["current_image_id"] = random_image.id  # Зберігаємо ID зображення у сесії
    else:
        random_image = ImageForGame.objects.get(id=request.session["current_image_id"])

    # Обробка POST-запиту, коли користувач робить свій вибір
    if request.method == "POST":
        user_guess = request.POST.get("class_guess")  # Отримуємо вибір користувача

        # Підготовка зображення для моделі (розмір, нормалізація тощо)
        image_path = random_image.image.path
        image = Image.open(image_path).resize((32, 32))  # Зміна розміру до 32x32
        image = np.array(image) / 255.0  # Нормалізація зображення
        image = np.expand_dims(image, axis=0)  # Додавання виміру для батчу

        # Отримуємо прогноз моделі
        prediction = model.predict(image)
        predicted_class_index = np.argmax(prediction)
        predicted_class = CLASSES[predicted_class_index]
        confidence = np.max(prediction) * 100  # Відсоток впевненості моделі

        # Перевірка правильності вибору користувача та моделі
        user_is_correct = user_guess == random_image.correct_label
        model_is_correct = predicted_class == random_image.correct_label

        # Оновлення рахунків
        if user_is_correct:
            request.session["user_score"] += 1
        if model_is_correct:
            request.session["model_score"] += 1

        # Очищення поточного зображення із сесії після завершення раунду
        del request.session["current_image_id"]

        # Передача результатів до шаблону
        context = {
            "image": random_image,  # Зображення, яке було використане у раунді
            "predicted_class": predicted_class,  # Клас, який передбачила модель
            "confidence": confidence,  # Впевненість моделі у своєму прогнозі
            "user_is_correct": user_is_correct,  # Чи вірно вгадав користувач
            "model_is_correct": model_is_correct,  # Чи вірно вгадала модель
            "user_score": request.session["user_score"],  # Рахунок користувача
            "model_score": request.session["model_score"],  # Рахунок моделі
            "title": _("Результат"),  # Заголовок сторінки
        }

        # Відображення результатів раунду
        return render(request, "game2/result.html", context)

    # Відображення основної сторінки гри з поточним зображенням
    return render(
        request,
        "game2/game.html",
        {"image": random_image, "title": _("Гра"), "page": "play_game", "app": "game2"},
    )


def reset_game(request):
    """
    Функція для скидання гри.
    Скидає всі сесійні дані та перенаправляє на початкову сторінку гри.
    """
    request.session.flush()  # Видаляє всі дані сесії
    return redirect("game2:play_game")  # Переходить на головну сторінку гри
