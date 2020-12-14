#!/bin/sh
python3 manage.py collectstatic --noinput
python manage.py makemigrations --merge --noinput
python manage.py makemigrations --noinput
python3 manage.py migrate --noinput
uwsgi --ini uwsgi.ini
