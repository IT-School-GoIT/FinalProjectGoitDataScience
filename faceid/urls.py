from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


app_name = "faceid"

urlpatterns = [
    path('', views.index, name='index'),
    path("login/", views.login, name="login"),
    path("signup/", views.register, name="register"),
    # path('logout/', views.user_logout, name='logout'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
