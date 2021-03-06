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
User.objects.create_superuser(username='admin', password='admin', email='admin@admin.test')"

# Start server
echo "Starting server"
python manage.py runserver 0.0.0.0:8000
