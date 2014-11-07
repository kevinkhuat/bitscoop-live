#!/bin/bash
# @authors Kyle Baran, Liam Broza


# Create installed checkpoints folder.
[ ! -d /installed ] && sudo mkdir /installed && sudo chmod -R 777 /installed

# Create packages folder.
[ ! -d /packages ] && sudo mkdir /packages && sudo chmod -R 777 /packages

[ -f /installed/Python-3.4.2 ] && echo Python-3.4.2 already installed. && exit 0

# Create packages folder.
[ ! -d /packages ] && sudo mkdir /packages

# Download source tarballs and signatures
[ ! -f /packages/Python-3.4.2.tgz ] && sudo wget -P /packages https://www.python.org/ftp/python/3.4.2/Python-3.4.2.tgz

# TODO: check hash of python tar
tar -xzf /packages/Python-3.4.2.tgz -C /packages
cd /packages/Python-3.4.2
# Configure install with the `with-ensurepip` flag set to install pip with Python (works with Python 3.4+)
sudo ./configure --with-ensurepip=install
make
sudo make altinstall
# Ensure pip package manager is up to date
sudo /usr/local/bin/pip3.4 install pip --upgrade
# Install virtualenv to manage virtual Python environments
sudo /usr/local/bin/pip3.4 install virtualenv

sudo touch /installed/Python-3.4.2
