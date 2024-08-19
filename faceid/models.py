from django.db import models

class UserPhoto(models.Model):
    name = models.CharField(max_length=255)
    photo = models.BinaryField()  # Store image data as binary

    def __str__(self):
        return self.name
