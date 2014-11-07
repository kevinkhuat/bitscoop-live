#!/bin/bash
# @authors Kyle Baran, Liam Broza

# Create installed checkpoints folder.
[ ! -d /installed ] && sudo mkdir /installed && sudo chmod -R 777 /installed

# Create packages folder.
[ ! -d /packages ] && sudo mkdir /packages && sudo chmod -R 777 /packages

# Install Passenger w/ nginx
[ -f /installed/passenger-4.0.53 && $1 != "force" ] && echo passenger-4.0.53 w/ nginx-1.7.7.tar.gz already installed. && exit 0

# Create packages folder.
[ ! -d /packages ] && sudo mkdir /packages

# Download source tarballs and signatures
[ ! -f passenger-4.0.53.tar.gz ] && sudo wget -P /packages https://s3.amazonaws.com/phusion-passenger/releases/passenger-4.0.53.tar.gz
[ ! -f nginx-1.7.7.tar.gz ] && sudo wget -P /packages http://nginx.org/download/nginx-1.7.7.tar.gz /packages

cd /packages

[ -d passenger-4.0.53 ] && rm -rf passenger-4.0.53
[ -d nginx-1.7.7 ] && rm -rf nginx-1.7.7

tar -xzf passenger-4.0.53.tar.gz
tar -xzf nginx-1.7.7.tar.gz

[ ! -d /opt/passenger ] && sudo mkdir /opt/passenger
sudo cp -r passenger-4.0.53/* /opt/passenger
sudo /opt/passenger/bin/passenger-install-nginx-module --auto --languages python --nginx-source-dir=./nginx-1.7.7

sudo touch /installed/passenger-4.0.53
sudo touch /installed/nginx-1.7.7

