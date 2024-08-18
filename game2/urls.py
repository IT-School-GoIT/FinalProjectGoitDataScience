from django.urls import path
from . import views

app_name = "game2"

urlpatterns = [
    path('play_game', views.play_game, name='play_game'),
    path('reset_game', views.reset_game, name='reset_game'),
    
]
