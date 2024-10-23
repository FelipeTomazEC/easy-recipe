#!/bin/bash

# Run migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput

# Start Gunicorn
gunicorn easy_recipe.wsgi --log-file -