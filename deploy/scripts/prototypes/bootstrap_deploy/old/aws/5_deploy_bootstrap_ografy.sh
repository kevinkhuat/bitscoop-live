#!/bin/sh
# @authors Kyle Baran, Liam Broza
cd /ografy
sudo curl -L -u mrhegemon:ntsupport5806 https://github.com/sjberry/ografy/archive/v0.1.0.tar.gz | sudo tar zx
sudo chown -R kbaran:kbaran /ografy
sudo chmod a+x /ografy
cd /ografy/ografy-0.1.0
yes | sudo /ografy/prod_env/bin/pip  install -r ografy/ografy-0.1.0/requirements/all.txt 
python manage.py migrate
python manage.py validate
python manage.py collectstatic
