#!/bin/bash
# @authors Kyle Baran, Liam Broza

# Create installed checkpoints folder.
[ ! -d /installed ] && sudo mkdir /installed && sudo chmod -R 777 /installed

# Create packages folder.
[ ! -d /packages ] && sudo mkdir /packages && sudo chmod -R 777 /packages

# Install Passenger w/ conf
[ -f /installed/passenger-4.0.53 ] && [ "$1" != "force" ] && echo passenger-4.0.53 w/ nginx-1.7.7.tar.gz already installed. && exit 0

if [ "$1" != "force" ]
then
    [ -d /packages/passenger-4.0.53 ] && rm -rf /packages/passenger-4.0.53
    [ -d /packages/nginx-1.7.7 ] && rm -rf /packages/nginx-1.7.7
fi

# Create packages folder.
[ ! -d /packages ] && sudo mkdir /packages

# Download source tarballs and signatures
[ ! -f passenger-4.0.53.tar.gz ] && wget -P /packages https://s3.amazonaws.com/phusion-passenger/releases/passenger-4.0.53.tar.gz
[ ! -f nginx-1.7.7.tar.gz ] && wget -P /packages http://nginx.org/download/nginx-1.7.7.tar.gz

tar -xzf /packages/passenger-4.0.53.tar.gz -C /packages
tar -xzf /packages/nginx-1.7.7.tar.gz -C /packages

[ ! -d /opt/passenger ] && sudo mkdir /opt/passenger
sudo cp -r /packages/passenger-4.0.53/* /opt/passenger
sudo /opt/passenger/bin/passenger-install-nginx-module --auto --languages python --nginx-source-dir=/packages/nginx-1.7.7

touch /installed/passenger-4.0.53
touch /installed/nginx-1.7.7
