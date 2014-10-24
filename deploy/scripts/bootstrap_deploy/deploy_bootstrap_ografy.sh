#!/bin/sh
# This file bootstraps deployment from vagrantfile for dev test and production
# @authors Kyle Baran, Liam Broza
curl https://raw.github.com/pypa/pip/master/contrib/get-pip.py | sudo python3.4 -
mkdir "ografy"
cd ografy
git clone 'https://'$1'@github.com/sjberry/ografy.git'
pip install -r requirements.txt 
python3.4 manage.py migrate
python3.4 manage.py validate
