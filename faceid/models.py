from django.contrib.auth.models import User
from django.db import models

class UserPhoto(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    photo = models.BinaryField()  # Store image data as binary

    def __str__(self):
        return self.user.username
    

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    victories = models.IntegerField(default=0)    
