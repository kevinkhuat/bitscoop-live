# This file bootstraps deployment from vagrantfile for dev test and production
# @authors Kyle Baran, Liam Broza

yum update
mkdir ografy
cd ografy
git clone https://username:password@github.com/sjberry/ografy.git
# Create the python 2.7 virtualenv
# Todo: Write check to ensure using Python 2.7
pip install virtualenv
# Install necessary development tool compiler for C compiler and install Python 3 for production virtual environment
yum groupinstall -y development
wget https://www.python.org/ftp/python/3.4.1/Python-3.4.1.tar.xz
xz -d Python-3.4.1.tar.xz
tar -xvf Python-3.4.1.tar
cd Python-3.4.1
./configure
make && make altinstall
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

# Installing Passenger through bullshit Ruby Rake nonsense.
# todo WILL FIX AND PUT INTO FABRIC FILE LATER
# https://www.phusionpassenger.com/documentation/Users%20guide%20Nginx.html#tarball_generic_install
yum install ruby rubygem-rake
mkdir /opt/passenger
cd /opt/passenger
tar xzvf /location-to/passenger-x.x.x.tar.gz
cd /opt/passenger/passenger-x.x.x
./bin/passenger-install-nginx-module
kill `cat /path-to/flying-passenger.pid`

python fab_deploy.py

deactivate