#!/bin/sh
# This file bootstraps deployment from vagrantfile for dev test and production
# @authors Kyle Baran, Liam Broza
#ToDo fix this for production. Don't run update each time because it takes forever.
#sudo yum update
# Install necessary development tool compiler for C compiler and install Python 3 for production virtual environment
sudo yum groupinstall -y development
curl https://bitbucket.org/pypa/setuptools/raw/bootstrap/ez_setup.py | sudo python -
# sudo pip install virtualenv
# TODO: Create the python 2.7 virtualenv
# Todo: Write check to ensure using Python 2.7
sudo wget https://www.python.org/ftp/python/3.4.1/Python-3.4.1.tar.xz
sudo xz -d Python-3.4.1.tar.xz
sudo tar -xvf Python-3.4.1.tar
cd Python-3.4.1
sudo ./configure
sudo make && sudo make altinstall
cd ..
curl https://raw.github.com/pypa/pip/master/contrib/get-pip.py | sudo python3.4 -
mkdir "ografy"
cd ografy
git clone 'https://'$1'@github.com/sjberry/ografy.git'
pip install -r requirements.txt
python3.4 manage.py syncdb
python3.4 manage.py validate
