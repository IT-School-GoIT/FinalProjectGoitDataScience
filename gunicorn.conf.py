# gunicorn.conf.py

# Вкажіть кількість воркерів
workers = 4

# Вкажіть тип воркерів
worker_class = 'gunicorn.workers.ggevent.GeventWorker'

# Вкажіть хост і порт
bind = '0.0.0.0:8001'

# Логування
accesslog = '-'
errorlog = '-'

# Налаштування таймаутів
timeout = 120
