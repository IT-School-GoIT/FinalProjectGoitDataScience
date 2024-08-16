from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import requests
import environ
import os
from pathlib import Path

# Визначення базового каталогу проекту
BASE_DIR = Path(__file__).resolve().parent.parent

# Ініціалізація середовища
env = environ.Env(DEBUG=(bool, False))
environ.Env.read_env(os.path.join(BASE_DIR, ".env"))

# Завантаження змінних оточення
API_KEY = env("API_KEY", default=None)

if not API_KEY:
    raise ValueError("API_KEY не знайдений. Перевірте файл .env")


def chat_page(request):
    return render(request, 'gpt_response/chat.html',
        {"title": "Чат Бот", "page": "chat_page", "app": "gpt_response"},)  # Рендеримо HTML-шаблон

@csrf_exempt
def chat_view(request):
    if request.method == 'POST':
        user_input = request.POST.get('input')

        # Запит до OpenAI API
        response = requests.post(
            'https://api.openai.com/v1/chat/completions',  # Використовуємо новий endpoint для GPT-3.5-turbo
            headers={
                'Authorization': f'Bearer {API_KEY}',
            },
            json={
                'model': 'gpt-4o-mini',
                'messages': [{"role": "user", "content": user_input}],
                'max_tokens': 150
            }
        )

        # Логування відповіді API
        data = response.json()
        print("Response from API:", data)  # Додамо логування для відслідковування відповіді

        if 'choices' not in data:
            return JsonResponse({'error': 'API response did not contain choices'}, status=500)

        generated_text = data['choices'][0]['message']['content']
        
        return JsonResponse({'response': generated_text})
    
    return JsonResponse({'error': 'Invalid request'}, status=400)