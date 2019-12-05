#!/bin/bash

set -e

python manage.py migrate

exec gunicorn -b 0.0.0.0:8080 voluntariapp_api.wsgi