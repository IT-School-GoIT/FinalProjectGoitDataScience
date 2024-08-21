from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = "accounts"

urlpatterns = [
    path("login/", views.login, name="login"),
    # path("logout/", views.logout, name="logout"),
    path("signup/", views.signup, name="signup"),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('user/<str:username>/', views.user_profile, name='user_profile'),

]