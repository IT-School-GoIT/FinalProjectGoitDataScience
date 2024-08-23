"""
Models for storing user data and photos for face recognition.

This module defines models that store user profile information 
and binary data for face recognition photos.

Classes:
    UserPhoto: Stores the binary photo data for a user's face ID.
    UserProfile: Stores additional profile information like victories.
"""

from django.contrib.auth.models import User
from django.db import models

class UserPhoto(models.Model):
    """
    Model for storing the binary photo data for face recognition.
    
    Attributes:
        user: A one-to-one relationship with the Django user.
        photo: Binary field to store the image data.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    photo = models.BinaryField()  # Store image data as binary

    def __str__(self):
        return self.user.username
    

class UserProfile(models.Model):
    """
    Model for storing additional user profile information.
    
    Attributes:
        user: A one-to-one relationship with the Django user.
        victories: Stores the number of victories achieved by the user.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    victories = models.IntegerField(default=0)    
