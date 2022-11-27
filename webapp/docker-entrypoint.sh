#!/bin/bash

# Collect static files
echo "Collect static files"
python manage.py collectstatic --noinput

# Apply database migrations
echo "Apply database migrations"
python manage.py migrate
echo "Load fixtures"
python manage.py loaddata observables

python manage.py shell -c "from django.contrib.auth.models import User;
from django.db.utils import IntegrityError
try:
    User.objects.create_superuser(username='${DJANGO_ADMIN_NAME}', password='${DJANGO_ADMIN_PASSWORD}', email='admin@admin.test')
except IntegrityError:
    pass"


# Start server
echo "Starting server"
# python manage.py runserver 0.0.0.0:8000
gunicorn --bind :8000 --workers 1 "irrigation.wsgi:application"
