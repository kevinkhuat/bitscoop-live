#!/bin/bash
# @authors Kyle Baran, Liam Broza


# Prep SSL by manually executing these commands on host machine and copying in the certs to www root
# TODO: Make programatic / add real signed certs
# sudo openssl genrsa -des3 -out server.key 1024
# sudo openssl req -new -key server.key -out server.csr
# sudo cp server.key server.key.org
# sudo openssl rsa -in server.key.org -out server.key
# sudo openssl x509 -req -days 365 -in server.csr -signkey server.key -out server.crt
# TODO: Copy certs to correct dir


# Update OS
sudo yum update -y


# Install package dependencies

# Compiles C packages (e.g. Python) from source
sudo yum install -y gcc
# Compiles C++ (e.g. Passenger) from source
sudo yum install -y gcc-c++
# Git clone Ografy repository
#sudo yum install -y git
# Passenger bindings
sudo yum install -y libcurl-devel
# Required for the installation of `pip` with Python make and SSL signing
# CentOS equivalent of `libssl-devel`
sudo yum install -y openssl-devel
# Passenger runtime and build dependency
sudo yum install -y ruby
# Required to install gem requirements
sudo yum install -y rubygem-rake
# Bindings required for building Passenger
sudo yum install -y ruby-devel
# Required for compiling Python sqlite3 bindings
sudo yum install -y sqlite-devel
# Used to download source dependencies
sudo yum install -y wget
# Passenger bindings
sudo yum install -y zlib-devel


# Additional Passenger gem dependances
sudo /usr/bin/gem install -y daemon_controller
sudo /usr/bin/gem install -y rack


# Download source tarballs and signatures
# TODO: Check file for existence (e.g. we don't want a Python-3.4.2.tgz.1)
# FIXME: For now scp a tar'd copy of the local working Ografy repo into virtual machine.
#curl -L -u 18412743985:DolfinParty9 https://github.com/sjberry/ografy/archive/v0.1.0.tar.gz > ografy.tar.gz
wget https://s3.amazonaws.com/phusion-passenger/releases/passenger-4.0.53.tar.gz
wget https://www.python.org/ftp/python/3.4.2/Python-3.4.2.tgz
wget https://www.python.org/ftp/python/3.4.2/Python-3.4.2.tgz.asc


# Extract Ografy tarball (there are development cert files and configurations necessary for other build steps)
tar -xzf ografy.tar.gz


# Import Python release manager/verifier PGP keys
# TODO: Fail on bad condition
gpg --recv-keys 6A45C816 36580288 7D9DC8D2 18ADD4FF A4135B38 A74B06BF EA5BBD71 ED9D77D5 E6DF025C 6F5E1540 F73C700D
# TODO: Import other PGP keys as required.


# Verify downloaded files where possible
# TODO: Fail on bad condition
gpg --verify Python-3.4.2.tgz.asc
# TODO: Verify Passenger tarball?


# Configure Python install, build binaries from source, and install
tar -xzf Python-3.4.2.tgz
cd Python-3.4.2
./configure
make
# Install package with the `with-ensurepip` flag set to install pip with Python (works with Python 3.4+)
sudo make altinstall --with-ensurepip=install
# Ensure pip package manager is up to date
sudo /usr/local/bin/pip3.4 install pip
# Install virtualenv to manage virtual Python environments
sudo /usr/local/bin/pip3.4 install virtualenv
cd ..


# Install Passenger w/ nginx
tar -xzf passenger-4.0.53.tar.gz
cd passenger-4.0.53
sudo mkdir /opt/passenger
yes | sudo ./bin/passenger-install-nginx-module --languages python
export PATH="$PATH:/opt/nginx/sbin"
cd ..


# Copy in Passenger and nginx configurations
sudo cp -r ografy/deploy/scripts/files/nginx /etc/init.d
sudo chmod +x /etc/init.d/nginx
sudo mkdir /opt/nginx/conf
sudo cp -r ografy/deploy/scripts/files/nginx.conf /opt/nginx/conf


# Create Python virtual environments
mkdir environments
cd environments
virtualenv --no-site-packages ografy.dev-3.4
#virtualenv --no-site-packages ografy.test-3.4
#virtualenv --no-site-packages ografy.prod-3.4
cd ..


# Prepare Ografy project
mkdir sites
mkdir sites/ografy.io
mkdir sites/ografy.io/www
mkdir sites/ografy.io/www/public
mkdir sites/ografy.io/www/tmp
mv ografy sites/ografy.io/www


# Install Ografy dependencies with pip and set up application
source environments/ografy.dev-3.4/bin/activate
pip install -r ografy/requirements/manual.txt
yes | python manage.py migrate
yes | python manage.py validate
yes | python manage.py collectstatic
deactivate
mv build/static/* sites/ografy.io/www/public


# Cleanup install script cruft
#rm Python-3.4.2.tgz
#rm Python-3.4.2.tgz.asc
#rm -rf Python-3.4.2


# Knock down the house of cards
sudo systemctl daemon-reload
sudo /etc/init.d/nginx start
