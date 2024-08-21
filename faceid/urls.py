from django.urls import path
from . import views


app_name = "faceid"

urlpatterns = [
    path('', views.index, name='index'),
    path("login/", views.login, name="login"),
    path("signup/", views.register, name="register"),
    path('logout/', views.user_logout, name='logout'),
]
