from django import forms
from .models import CustomUser


class FaceRegistrationForm(forms.Form):
    face_image = forms.ImageField()


class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'image', 'password']
