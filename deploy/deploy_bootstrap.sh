#!/bin/sh
# This file bootstraps deployment from vagrantfile for dev test and production
# @authors Kyle Baran, Liam Broza
#Don't run update each time because it takes forever.
#ToDo fix this for production
#sudo yum update
# Install necessary development tool compiler for C compiler and install Python 3 for production virtual environment
sudo yum groupinstall -y development
sudo yum -y install python-pip
curl https://bitbucket.org/pypa/setuptools/raw/bootstrap/ez_setup.py | sudo python -
curl https://raw.github.com/pypa/pip/master/contrib/get-pip.py | sudo python -
sudo pip install virtualenv
sudo mkdir -p "ografy"
cd ografy
sudo git clone https://barankyle:Foxtrot0196@github.com/sjberry/ografy.git
# Create the python 2.7 virtualenv
# Todo: Write check to ensure using Python 2.7
sudo wget https://www.python.org/ftp/python/3.4.1/Python-3.4.1.tar.xz
sudo xz -d Python-3.4.1.tar.xz
sudo tar -xvf Python-3.4.1.tar
cd Python-3.4.1
sudo ./configure
sudo make && sudo make altinstall