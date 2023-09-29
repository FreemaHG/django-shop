#!/bin/bash

# Сбор статических файлов для последующей обработки сервером nginx
python3 -m app.manage collectstatic --noinput

# Запуск сервера
gunicorn app.megano.wsgi:application --workers 4 --bind=0.0.0.0:8000
