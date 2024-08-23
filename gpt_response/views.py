"""
views.py
--------

This module handles the views for the GPT-4 interaction page, including rendering the chat interface 
and processing requests to the OpenAI API to generate responses.

Functions:
----------

- `chat_page(request)`:
    Renders the chat page where users can interact with the GPT-4 model. This view is protected by the 
    `login_required` decorator to ensure that only authenticated users can access it.

- `chat_view(request)`:
    Handles POST requests from the chat interface, sends user input to the GPT-4 model via the OpenAI API, 
    and returns the AI-generated response as a JSON object.

Dependencies:
-------------
- `requests`: Used to interact with external APIs (OpenAI GPT-4 API).
- `environ`: For handling environment variables, particularly loading the API key from a `.env` file.
- `os`: To work with file paths and environment settings.
- `csrf_exempt`: To allow the chat interaction view to bypass CSRF validation.
- `login_required`: Ensures that only logged-in users can access the chat page.

Variables:
----------

- `API_KEY`: The API key required to interact with the OpenAI GPT-4 model. Loaded from the `.env` file.

"""

from django.utils.translation import gettext as _
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import requests
import environ
import os
from pathlib import Path

# Визначення базового каталогу проекту
BASE_DIR = Path(__file__).resolve().parent.parent

# Ініціалізація середовища для завантаження змінних із .env файлу
env = environ.Env(DEBUG=(bool, False))
environ.Env.read_env(os.path.join(BASE_DIR, ".env"))  # Завантаження .env файлу з кореневої директорії

# Завантаження значення API_KEY з .env файлу
API_KEY = env("API_KEY", default=None)

# Перевірка наявності значення API_KEY, якщо не знайдено — викликається помилка
if not API_KEY:
    raise ValueError("API_KEY не знайдений. Перевірте файл .env")

@login_required
def chat_page(request):
    """
    Renders the chat page where users can interact with the GPT-4 model.
    
    Args:
        request (HttpRequest): The HTTP request object.
        
    Returns:
        HttpResponse: The rendered HTML page for the chat interface.
        
    This function uses the 'gpt_response/chat.html' template and injects the page title, page id, and app name.
    It is protected by the `login_required` decorator, so only authenticated users can access the page.
    """
    return render(request, 'gpt_response/chat.html',
        {"title": _("Чат Бот"), "page": "chat_page", "app": "gpt_response"},)  # Рендеримо HTML-шаблон сторінки чату

@csrf_exempt
def chat_view(request):
    """
    Processes POST requests for interacting with the OpenAI GPT API to generate responses.
    
    Args:
        request (HttpRequest): The HTTP request object. The function expects a POST request containing
                               user input via the 'input' field.
    
    Returns:
        JsonResponse: A JSON response containing the AI-generated text or an error message.
        
    This view handles requests to interact with the GPT model using the OpenAI API. It receives user input, 
    sends it to the OpenAI API, and returns the generated response as a JSON object.
    """
    if request.method == 'POST':
        # Отримання тексту запиту від користувача
        user_input = request.POST.get('input')

        # Запит до OpenAI API з використанням моделі GPT-4o-mini
        response = requests.post(
            'https://api.openai.com/v1/chat/completions',  # Використовується endpoint для GPT
            headers={
                'Authorization': f'Bearer {API_KEY}',  # Передаємо API ключ у заголовку запиту
            },
            json={
                'model': 'gpt-4o-mini',  # Вказуємо модель для генерації відповідей
                'messages': [{"role": "user", "content": user_input}],  # Передаємо повідомлення від користувача
                'max_tokens': 150  # Обмежуємо кількість згенерованих токенів
            }
        )

        # Логування відповіді від API
        data = response.json()
        print("Response from API:", data)  # Виводимо відповідь API у консоль для налагодження

        # Перевіряємо наявність ключа 'choices' у відповіді API
        if 'choices' not in data:
            return JsonResponse({'error': 'API response did not contain choices'}, status=500)

        # Отримання згенерованого тексту від моделі
        generated_text = data['choices'][0]['message']['content']
        
        # Відправляємо згенерований текст як JSON відповідь
        return JsonResponse({'response': generated_text})
    
    # Якщо метод запиту не POST, повертаємо помилку
    return JsonResponse({'error': 'Invalid request'}, status=400)
