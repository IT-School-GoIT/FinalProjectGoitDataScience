"""
URL configuration for the faceid application.

This module defines the URL patterns for the face ID authentication 
system, including views for index, login, and registration.

URLs:
    index: Main page for uploading images.
    login: Page for user login with face ID.
    signup: Page for user registration with face ID.
    logout: Logout functionality using Django's built-in view.
"""

from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = "faceid"

urlpatterns = [
    path('', views.index, name='index'),
    path("login/", views.login, name="login"),
    path("signup/", views.register, name="register"),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
