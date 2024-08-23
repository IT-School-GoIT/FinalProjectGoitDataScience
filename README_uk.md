# Cognition Creators - Image Classification Web Service
- [Read in English](README_en.md)

## Опис проекту

Cognition Creators - це багатофункціональний веб-сервіс, що використовує сучасні технології штучного інтелекту для класифікації зображень та взаємодії з користувачами. Основою проекту є згорткові нейронні мережі (CNN), які дозволяють класифікувати зображення на основі тренованих моделей. Сервіс надає користувачам можливість завантажувати зображення, тренувати моделі, отримувати результати класифікації з високою точністю, а також взаємодіяти з сервісом через додаткові функції.

Проект також включає інтерактивний чат, побудований на базі GPT-4, який дозволяє користувачам отримувати відповіді на запитання та вести діалоги з штучним інтелектом. Для авторизації користувачів впроваджено інноваційне рішення за допомогою Face ID, що забезпечує безпечний доступ до сервісу. Додатково, користувачі можуть грати в інтерактивну гру, що демонструє можливості нейронних мереж в режимі реального часу.

Сервіс призначений для дослідників, розробників та ентузіастів штучного інтелекту, а також для будь-якого користувача, який бажає дослідити можливості машинного навчання та штучного інтелекту у зручному та доступному веб-інтерфейсі.

## Основні функції

- **Завантаження зображень:** Користувачі можуть завантажувати зображення для класифікації.
- **Тренування моделей:** Модель CNN тренується на основі датасету CIFAR-10.
- **Перевірка зображень:** Модель класифікує зображення і відображає результати з високою точністю.
- **Контейнеризація:** Проект повністю контейнеризований за допомогою Docker, що забезпечує простоту розгортання.
- **Авторизація:** Користувачі можуть реєструватися, входити та виходити з системи.
- **Face ID:** Реалізована можливість реєстрації та авторизації за допомогою Face ID на основі зображень з камери.
- **Гра:** Інтерактивна гра з використанням нейронної мережі.
- **Чат на базі GPT-4:** Інтерактивний чат із використанням штучного інтелекту GPT-4, доступний лише для авторизованих користувачів.

## Використані технології

- **Python:** Основна мова програмування для реалізації логіки та нейронної мережі.
- **Django:** Веб-фреймворк для створення серверної частини та управління веб-інтерфейсом.
- **Convolutional Neural Networks (CNN):** Згорткові нейронні мережі для класифікації зображень.
- **PostgreSQL:** Система управління базами даних для зберігання результатів класифікації та даних користувачів.
- **Docker:** Інструмент для контейнеризації додатку.
- **GitHub:** Платформа для спільної роботи та контролю версій.
- **Agile:** Методологія розробки проекту.
- **HTML/CSS/JavaScript:** Для побудови фронтенд-частини, включаючи інтерактивні елементи, такі як модальні вікна та перемикач мови.
- **Bootstrap:** Фреймворк для створення адаптивного веб-дизайну.
- **Mediapipe:** Технологія для обробки зображень з камери та реалізації Face ID.
- **Pillow (PIL):** Бібліотека Python для обробки зображень, включаючи їх масштабування та форматування.
- **JWT (JSON Web Tokens):** Технологія для безпечної авторизації користувачів.
- **GPT-4 API:** Використовується для реалізації інтерактивного чату з штучним інтелектом.
- **Koyeb:** Платформа для хостингу та розгортання додатку.

## Інструкція з встановлення

1. Клонувати репозиторій:
   ```bash
   git clone https://github.com/IT-School-GoIT/final_data_science_goit.git
   cd final_data_science_goit

2. Створити та активувати віртуальне середовище:
   ```bash
   python3 -m venv env
   source env/bin/activate  # На Windows використовуйте команду `env\Scripts\activate`

3. Встановити залежності:
   ```bash
   pip install -r requirements.txt

4. Налаштувати базу даних:
   Створіть файл .env із своїми даними
   Відредагуйте файл root/settings.py(якщо є така необхідність), щоб налаштувати підключення до PostgreSQL.

5. Міграції бази даних:
   ```bash
   python manage.py migrate

6. Запустити сервер розробки:
   ```bash
   python manage.py runserver


## Release plan
- Release 0.1 - Start
- Release 1.0 - implement features from 1 to 9
- Release 1.1 - implement feature 10
- Release 1.2 - implement feature 11-13
- Release 2.0 - implement user iteraction interface (replace terminal commands iteraction)


## Branch naming
Use feature / release flow style Example: branch name to work on feature feature/Ticket## branch name for releale releale/release-1.0 major branch always main

1. Keep main always in working condition (No errors,failures allowed) , merge into main releale branches only after PR approves from team members , merged branch should be green .
2. Never!!!!! rename main branch
3. To start work on new feature ticket , create new branch from upcoming release branch . When work on feature done , create Pull Request into release branch , add reviewers into your PR. After work on PR comments and final approves from team merge feature branch into release branch.
4. Do not temper to add comments into your code . Team members will appreciate your work.
