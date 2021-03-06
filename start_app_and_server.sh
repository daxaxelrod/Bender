#!/bin/bash

# sits in /etc/rc.local which fires on boot

cd /home/pi/Documents/bender

# git pull

# pipenv install

# could use gunicorn here but runserver better for debugging
pipenv run python manage.py runserver 0.0.0.0:8000  --noreload &

cd app/templates/bender-ui

serve -s build &

# add --kiosk to disable f11
#chromium-browser --start-fullscreen http://localhost:5000 &

