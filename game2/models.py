from django.db import models


class ImageForGame(models.Model):
    """
    Клас ImageForGame представляє модель для зберігання зображень,
    що використовуються в грі, та їхніх правильних відповідей (correct_label).

    Поля:
    - title: Назва зображення (рядок до 255 символів), за замовчуванням "Untitled".
    - image: Зображення, яке завантажується у папку 'game_images/'.
    - correct_label: Правильний клас для цього зображення (рядок до 50 символів).
    """

    title = models.CharField(max_length=255, default="Untitled")
    image = models.ImageField(upload_to="game_images/")
    correct_label = models.CharField(max_length=50)

    def __str__(self):
        """
        Метод для повернення назви зображення при його представленні у вигляді рядка.
        """
        return self.title
