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
[ ! -n "`gem list | grep daemon_controller`" ] && yes | sudo /usr/bin/gem install daemon_controller
[ ! -n "`gem list | grep rack`" ] && yes | sudo /usr/bin/gem install rack


# Download source tarballs and signatures
# FIXME: For now scp a tar'd copy of the local working Ografy repo into virtual machine.
[ ! -f ografy.tar.gz ] && echo "File ografy.tar.gz not found. Aborting..." && exit 1
#curl -L -u 18412743985:DolfinParty9 https://github.com/sjberry/ografy/archive/v0.1.0.tar.gz > ografy.tar.gz
[ ! -f passenger-4.0.53.tar.gz ] && wget https://s3.amazonaws.com/phusion-passenger/releases/passenger-4.0.53.tar.gz
[ ! -f Python-3.4.2.tgz ] && wget https://www.python.org/ftp/python/3.4.2/Python-3.4.2.tgz
#[ ! -f Python-3.4.2.tgz.asc ] && wget https://www.python.org/ftp/python/3.4.2/Python-3.4.2.tgz.asc


# Import PGP keys
# TODO: Don't reimport if you've already retrieved keys.
# TODO: Fail on bad condition
# Python release managers/verifiers
#gpg --recv-keys 6A45C816 36580288 7D9DC8D2 18ADD4FF A4135B38 A74B06BF EA5BBD71 ED9D77D5 E6DF025C 6F5E1540 F73C700D
# TODO: Import Passenger PGP keys.
# TODO: Import our own PGP key?


# Verify downloaded files where possible
# TODO: Don't reverify if you've already verified.
# TODO: Fail on bad condition
#gpg --verify Python-3.4.2.tgz.asc
# TODO: Verify Passenger tarball?
# TODO: Verify Ografy tarball? Do we care about signing our own source? How paranoid do we want to get?


# Extract Ografy tarball (there are development cert files and configurations necessary for other build steps)
[ ! -d ografy ] && tar -xzf ografy.tar.gz


# Create checkpoints folder.
[ ! -d checkpoints ] && mkdir checkpoints


# Configure Python install, build binaries from source, and install
if [ ! -f checkpoints/python ]
then
    [ -d Python-3.4.2 ] &&  rm -rf Python-3.4.2

    tar -xzf Python-3.4.2.tgz
    cd Python-3.4.2
    # Configure install with the `with-ensurepip` flag set to install pip with Python (works with Python 3.4+)
    ./configure --with-ensurepip=install
    make
    sudo make altinstall
    # Ensure pip package manager is up to date
    sudo /usr/local/bin/pip3.4 install pip
    # Install virtualenv to manage virtual Python environments
    sudo /usr/local/bin/pip3.4 install virtualenv
    cd ..

    touch checkpoints/python
fi


# Install Passenger w/ nginx
if [ ! -f checkpoints/passenger ]
then
    [ -d passenger-4.0.53 ] && rm -rf passenger-4.0.53

    tar -xzf passenger-4.0.53.tar.gz
    [ ! -d /opt/passenger ] && sudo mkdir /opt/passenger
    sudo cp -r passenger-4.0.53 /opt/passenger
    yes | sudo /opt/passenger/passenger-4.0.53/bin/passenger-install-nginx-module --languages python
    export PATH="$PATH:/opt/nginx/sbin"

    touch checkpoints/passenger
fi


# Configure Passenger install in Passenger and nginx configurations
sudo cp ografy/deploy/scripts/files/nginx /etc/init.d
sudo chmod +x /etc/init.d/nginx
[ ! -d /opt/nginx/conf ] && sudo mkdir /opt/nginx/conf
sudo cp ografy/deploy/scripts/files/nginx.conf /opt/nginx/conf


# Create Python virtual environments
if [ ! -d environments ]
then
    mkdir environments
    cd environments
    # TODO: Environment toggle.
    /usr/local/bin/virtualenv --no-site-packages ografy.dev-3.4
    #/usr/local/bin/virtualenv --no-site-packages ografy.test-3.4
    #/usr/local/bin/virtualenv --no-site-packages ografy.prod-3.4
    cd ..
fi


# Install Ografy dependencies with pip and set up application
source environments/ografy.dev-3.4/bin/activate
pip install -r ografy/requirements/manual.txt
yes | python ografy/manage.py migrate
yes | python ografy/manage.py validate
yes yes | python ografy/manage.py collectstatic
deactivate


# Deploy Ografy project
[ ! -d sites ] && mkdir sites
[ ! -d sites/ografy.io ] && mkdir sites/ografy.io
[ ! -d sites/ografy.io/www ] && mkdir sites/ografy.io/www
[ ! -d sites/ografy.io/www/public ] && mkdir sites/ografy.io/www/public
[ ! -d sites/ografy.io/www/tmp ] && mkdir sites/ografy.io/www/tmp
mv -f ografy/build/static/* sites/ografy.io/www/public
cp -r ografy sites/ografy.io/www && mv sites/ografy.io/www/ografy/passenger_wsgi.py sites/ografy.io/www


# Knock down the house of cards
sudo /opt/nginx/sbin/nginx -s reload


# Cleanup install script cruft if everything succeeds
#rm ografy.tar.gz
#rm -rf ografy
#rm passenger-4.0.53.tar.gz
#rm -rf passenger-4.0.53
#rm Python-3.4.2.tgz
#rm Python-3.4.2.tgz.asc
#rm -rf Python-3.4.2
#rm -rf checkpoints
