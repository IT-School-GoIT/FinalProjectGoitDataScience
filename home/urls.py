from django.urls import path
from . import views

app_name = "home"

urlpatterns = [
    path("", views.index, name="index"),
    path("team/", views.team, name="team"),
    path("cognition/", views.cognition, name="cognition"),

]