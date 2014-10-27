#!/bin/sh
# @authors Kyle Baran, Liam Broza
# TODO: Standardize these folders
source /ografy/ografy_env/bin/activate
cd /home/kbaran/shared/
yes | sudo /ografy/ografy_env/bin/pip  install -r requirements/all.txt
yes | python manage.py migrate
yes | python manage.py validate
yes yes | sudo /ografy/ografy_env/bin/python3.4 manage.py collectstatic
