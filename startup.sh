#!/bin/bash


sudo /usr/sbin/nginx

source activate hydroserver
cd /home/hsapp/hydroserver
./hydroserver.sh
