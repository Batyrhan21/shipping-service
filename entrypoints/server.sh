#!/bin/sh
cd src
echo "Создаю миграции..."
python manage.py makemigrations

echo "Отправляю миграции..."
python manage.py migrate

echo "Собираю статику..."
python manage.py collectstatic --no-input

echo "Выгружаю данные из файла csv"
python manage.py unload_locations ../uszips.csv

echo "Cron schedule start"
python manage.py runcrons

echo "Запускаю сервер..."
gunicorn shipping.wsgi --bind 0.0.0.0:8000 --reload