from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = "accounts"

urlpatterns = [
    path("login/", views.login, name="login"),
    path("signup/", views.signup, name="signup"),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),  # Using Django's default logout view
    path('user/<str:username>/', views.user_profile, name='user_profile'),  # User profile view based on username
]
