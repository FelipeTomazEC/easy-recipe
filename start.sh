#!/bin/bash

# Run migrations
python manage.py migrate

# Start Gunicorn
gunicorn easy_recipe.wsgi --log-file -