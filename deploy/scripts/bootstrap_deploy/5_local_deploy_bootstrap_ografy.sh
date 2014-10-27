#!/bin/sh
# @authors Kyle Baran, Liam Broza
source /ografy/ografy_env/bin/activate
cd /mnt/hgfs/williambroza/DEV/Repos/ografy/
yes | sudo /ografy/ografy_env/bin/pip  install -r requirements/all.txt
python manage.py migrate
python manage.py validate
python manage.py collectstatic
