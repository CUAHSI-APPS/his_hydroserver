#!/bin/bash

# Start Gunicorn processes
echo Activating Environment
source activate hydroserver
echo Collecting Static Files
python manage.py collectstatic --noinput

echo Starting Gunicorn.
exec gunicorn hydroserver.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 3