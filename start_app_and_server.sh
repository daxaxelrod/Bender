#!/bin/bash

# sits in /etc/rc.local which fires on boot

cd /home/pi/Documents/bender

sudo git pull

# could use gunicorn here but runserver better for debugging
pipenv run python manage.py runserver --noreload

cd app/templates/bender-ui

npm start



