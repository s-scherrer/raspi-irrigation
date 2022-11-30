#!/bin/sh

# Collect static files
echo "Collect static files"
python manage.py collectstatic --noinput

# Apply database migrations
echo "Apply database migrations"
python manage.py migrate
echo "Load fixtures"
python manage.py loaddata observables

# Start server
echo "Starting server"
gunicorn --bind :8000 --workers 1 "irrigation.wsgi:application"
