#!/bin/sh
# @authors Kyle Baran, Liam Broza
# TODO: Standardize these folders
source /ografy/ografy_env/bin/activate
cd /home/kbaran/shared/
yes | sudo /ografy/ografy_env/bin/pip  install -r /home/kbaran/ografy/requirements/all.txt
yes | python /home/kbaran/ografy/manage.py migrate
yes | python /home/kbaran/ografy/manage.py validate
yes yes | sudo /ografy/ografy_env/bin/python3.4 /home/kbaran/ografy/manage.py collectstatic
