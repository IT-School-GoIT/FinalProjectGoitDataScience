from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
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

def chat_page(request):
    """
    Відображає сторінку чату.
    
    Аргументи:
    request (HttpRequest): Об'єкт HTTP запиту.
    
    Повертає:
    HttpResponse: Відрендерена HTML сторінка для чату.
    """
    return render(request, 'gpt_response/chat.html',
        {"title": "Чат Бот", "page": "chat_page", "app": "gpt_response"},)  # Рендеримо HTML-шаблон сторінки чату

@csrf_exempt
def chat_view(request):
    """
    Обробляє POST-запити до чату і взаємодіє з OpenAI API для генерації відповіді.
    
    Аргументи:
    request (HttpRequest): Об'єкт HTTP запиту, очікується метод POST з полем 'input'.
    
    Повертає:
    JsonResponse: JSON відповідь з згенерованим текстом або помилкою.
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
