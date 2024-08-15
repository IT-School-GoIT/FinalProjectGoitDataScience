from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView

app_name = "face_id"

urlpatterns = [
    path('register/', views.register, name='register'),  # Маршрут для реєстрації
    path('face_login/', views.face_login, name='face_login'),  # Маршрут для авторизації через обличчя
    # path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
