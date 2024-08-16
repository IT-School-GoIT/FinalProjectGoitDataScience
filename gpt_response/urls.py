from django.urls import path
from . import views

urlpatterns = [
    path('chat_page/', views.chat_page, name='chat_page'),  # Маршрут для HTML-сторінки
    path('chat/', views.chat_view, name='chat'),  # Маршрут для API чату
]
