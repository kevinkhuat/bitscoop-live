#!/bin/bash


[ ! -f ${HOME}/ografy.tar.gz ] && echo File ografy.tar.gz not found. Aborting... && exit 1
[ ! -f ${HOME}/static.tar.gz ] && echo File static.tar.gz not found. Aborting... && exit 1


if ! /usr/bin/id -g ografy &>/dev/null; then
    sudo /usr/sbin/groupadd -r ografy
fi

if ! /usr/bin/id ografy &>/dev/null; then
    sudo /usr/sbin/useradd -M -r -g ografy -d /var/lib/ografy -s /sbin/nologin -c ografy ografy > /dev/null 2>&1
fi

sudo usermod -a -G ografy nginx


umask 022
sudo rm -rf /var/lib/ografy/sites
sudo mkdir -p /var/{lib,log}/ografy
sudo mkdir -p /var/lib/ografy/environments
sudo mkdir -p /var/lib/ografy/sites/ografy.io/{static,www}/{public,tmp}


# Install source files.
sudo tar -xzvf ografy.tar.gz -C /var/lib/ografy/sites/ografy.io/www
sudo tar -xzvf static.tar.gz -C /var/lib/ografy/sites/ografy.io/static/public
sudo mv -v /var/lib/ografy/sites/ografy.io/www/ografy/passenger_wsgi.py /var/lib/ografy/sites/ografy.io/www/
sudo touch /var/lib/ografy/sites/ografy.io/www/tmp/restart.txt


# Adjust file/folder permissions.
sudo chown ografy:ografy -R /var/lib/ografy /var/log/ografy


# Create Python environment for ografy
if [ ! -f /var/lib/ografy/environments/ografy-3.4/bin/activate ]
then
    cd /var/lib/ografy/environments
    sudo rm -rf ografy-3.4
    sudo -u ografy /usr/local/bin/virtualenv --no-site-packages ografy-3.4
fi


# Install Ografy dependencies with pip and set up application
sudo -u ografy /var/lib/ografy/environments/ografy-3.4/bin/pip install -r /var/lib/ografy/sites/ografy.io/www/ografy/requirements/manual.txt
