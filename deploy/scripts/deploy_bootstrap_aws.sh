#!/bin/sh
# Create the virtualenv environment for Ografy
mkdir envs envs/fab envs/ografy
cd envs/ografy
virtualenv --python=/usr/bin/python3 --no-site-packages ografy_env
#Create virtualenv for Fabric
cd ../fab
virtualenv --no-site-packages fabric_env
source fabric_env/bin/activate
cd ../..
pip install fabric
pip install git+git://github.com/ronnix/fabtools.git
# Installing Passenger through Ruby Rake nonsense.
# todo WILL FIX AND PUT INTO FABRIC FILE LATER
# https://www.phusionpassenger.com/documentation/Users%20guide%20Nginx.html#tarball_generic_install
yum install ruby rubygem-rake
mkdir /opt/passenger
cd /opt/passenger
tar xzvf /location-to/passenger-x.x.x.tar.gz
cd /opt/passenger/passenger-x.x.x
./bin/passenger-install-nginx-module
kill `cat /path-to/flying-passenger.pid`
#Todo Add Passenger and Nginx to startup and then start Passenger
python ./fab_deploy.py
deactivate