#!/bin/bash
# @authors Kyle Baran, Liam Broza


[ ! -d /installed ] && sudo mkdir /installed
[ -f /installed/Python-3.4.2 && $1 != "force" ] && echo Python-3.4.2 already installed. && exit 0

# TODO: Check for sources folder

# Download source tarballs and signatures
[ ! -f Python-3.4.2.tgz ] && wget https://www.python.org/ftp/python/3.4.2/Python-3.4.2.tgz

# TODO: check hash of python tar
tar -xzf Python-3.4.2.tgz
cd Python-3.4.2
# Configure install with the `with-ensurepip` flag set to install pip with Python (works with Python 3.4+)
sudo ./configure --with-ensurepip=install
make
sudo make altinstall
# Ensure pip package manager is up to date
sudo /usr/local/bin/pip3.4 install pip --upgrade
# Install virtualenv to manage virtual Python environments
sudo /usr/local/bin/pip3.4 install virtualenv

cd ~/

touch /installed/Python-3.4.2
