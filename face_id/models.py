from django.db import models
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User, AbstractUser, Group, Permission
import numpy as np



class FaceProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    face_vector = models.BinaryField()  # Збереження вектора обличчя


# class CustomUser(models.Model):
#     username = models.CharField(max_length=150, unique=True)
#     email = models.EmailField(unique=True)
#     password = models.CharField(max_length=128)  # Поле для збереження хешованого паролю
#     image = models.ImageField(upload_to="user_images/", null=True, blank=True)  # Зображення обличчя
#     face_vector = models.BinaryField(null=True, blank=True)  # Вектор обличчя для авторизації

#     def set_password(self, raw_password):
#         """Метод для хешування паролю"""
#         self.password = make_password(raw_password)

#     def __str__(self):
#         return self.username


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    image = models.ImageField(upload_to="profile_images/", blank=True, null=True)
    face_vector = models.BinaryField(blank=True, null=True)

    groups = models.ManyToManyField(
        Group,
        related_name="customuser_set",  # Додайте related_name тут
        blank=True,
        help_text=(
            "The groups this user belongs to. A user will get all permissions "
            "granted to each of their groups."
        ),
        verbose_name=("groups"),
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="customuser_permissions_set",  # Додайте related_name тут
        blank=True,
        help_text=("Specific permissions for this user."),
        verbose_name=("user permissions"),
    )

    def save_face_vector(self, face_vector):
        self.face_vector = np.array(face_vector).tobytes()
        self.save()
