#! /bin/bash
cd /home/pi/stereo
nohup python ./manage.py runserver 0.0.0.0:80 --noreload &
