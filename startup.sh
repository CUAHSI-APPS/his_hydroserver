#!/bin/bash


source /home/hsapp/miniconda2/bin/activate hydroserver

python /home/hsapp/hydroserver/manage.py collectstatic --noinput

/usr/bin/supervisord -c /home/hsapp/hydroserver/supervisord.conf
