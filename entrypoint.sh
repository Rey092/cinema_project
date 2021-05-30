#!/bin/bash

python src/manage.py makemigrations --no-input

python src/manage.py migrate --no-input

exec gunicorn --pythonpath src src.wsgi:application -b 0.0.0.0:8000 --reload
