#!/bin/sh
# This file bootstraps deployment from vagrantfile for dev test and production
# @authors Kyle Baran, Liam Broza
# TODO: Create the python 2.7 virtualenv
# Todo: Write check to ensure using Python 2.7
sudo cd /
sudo wget https://www.python.org/ftp/python/3.4.1/Python-3.4.1.tar.xz
sudo xz -d Python-3.4.1.tar.xz
sudo tar -xvf Python-3.4.1.tar
cd Python-3.4.1
sudo ./configure
sudo make && sudo make altinstall
cd /
export PATH="$PATH:/usr/local/bin/python3.4"
curl https://raw.github.com/pypa/pip/master/contrib/get-pip.py | sudo python3.4 -
sudo cd /
wget https://bootstrap.pypa.io/ez_setup.py -O - | sudo python3.4
sudo easy_install pip
