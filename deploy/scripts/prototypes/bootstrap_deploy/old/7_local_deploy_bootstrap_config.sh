#!/bin/sh
# @authors Kyle Baran, Liam Broza

echo export PYTHONPATH=~/ografy/ografy_env/bin/ >> ~/.bash_profile
sudo mkdir /opt/nginx/html/public
sudo cp -r passenger_wsgi.py /opt/nginx/html/public
