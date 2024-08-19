from django.conf.urls.i18n import set_language
from django.urls import path
from . import views

app_name = "home"

urlpatterns = [
    path("", views.index, name="index"),
    path("team/", views.team, name="team"),
    path("cognition/", views.cognition, name="cognition"),
    path("privacy_policy/", views.privacy_policy, name="privacy_policy"),
    path(
        "presentation_of_the_project/",
        views.presentation_of_the_project,
        name="presentation_of_the_project",
    ),
    path('set_language/', set_language, name='set_language'),
]

