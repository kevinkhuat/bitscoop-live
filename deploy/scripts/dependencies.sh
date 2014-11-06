#!/bin/bash
# @authors Kyle Baran, Liam Broza


# Establish variables
case "$1" in
    production)
        echo Using production settings.
        ;;
    virtual)
        echo Using virtual settings.
        ;;
    *)
        echo $"Usage: $0 {production|virtual}"
        exit 2
        ;;
esac


# Update OS
sudo yum update -y


# Install package dependencies

# Needed to decompress some pip dependencies.
sudo yum install -y bzip2-devel
# Compiles C packages (e.g. Python) from source
sudo yum install -y gcc
# Compiles C++ (e.g. Passenger) from source
sudo yum install -y gcc-c++
# Git clone Ografy repository
#sudo yum install -y git
# Passenger bindings
sudo yum install -y libcurl-devel
# Needed to sync time with global time
sudo yum install -y ntp ntpdate ntp-doc
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
# PostgreSQL tools
sudo yum install -y postgresql-devel


# Additional Passenger gem dependances
[ ! -n "`gem list | grep daemon_controller`" ] && yes | sudo /usr/bin/gem install daemon_controller
[ ! -n "`gem list | grep rack`" ] && yes | sudo /usr/bin/gem install rack


# Download source tarballs and signatures
#curl -L -u 18412743985:DolfinParty9 https://github.com/sjberry/ografy/archive/v0.1.0.tar.gz > ografy.tar.gz
[ ! -f Python-3.4.2.tgz ] && wget https://www.python.org/ftp/python/3.4.2/Python-3.4.2.tgz
[ ! -f passenger-4.0.53.tar.gz ] && wget https://s3.amazonaws.com/phusion-passenger/releases/passenger-4.0.53.tar.gz
[ ! -f nginx-1.7.7.tar.gz ] && wget http://nginx.org/download/nginx-1.7.7.tar.gz


# Create checkpoints folder.
[ ! -d checkpoints ] && mkdir checkpoints


# Configure Python install, build binaries from source, and install
if [ ! -f checkpoints/python ]
then
    [ -d Python-3.4.2 ] && rm -rf Python-3.4.2

    tar -xzf Python-3.4.2.tgz
    cd Python-3.4.2
    # Configure install with the `with-ensurepip` flag set to install pip with Python (works with Python 3.4+)
    ./configure --with-ensurepip=install
    make
    sudo make altinstall
    # Ensure pip package manager is up to date
    sudo /usr/local/bin/pip3.4 install pip --upgrade
    # Install virtualenv to manage virtual Python environments
    sudo /usr/local/bin/pip3.4 install virtualenv
    cd ..

    touch checkpoints/python
fi


# Install Passenger w/ nginx
if [ ! -f checkpoints/passenger ]
then
    [ -d passenger-4.0.53 ] && rm -rf passenger-4.0.53
    [ -d nginx-1.7.7 ] && rm -rf nginx-1.7.7

    tar -xzf passenger-4.0.53.tar.gz
    tar -xzf nginx-1.7.7.tar.gz

    [ ! -d /opt/passenger ] && sudo mkdir /opt/passenger
    sudo cp -r passenger-4.0.53/* /opt/passenger
    sudo /opt/passenger/bin/passenger-install-nginx-module --auto --languages python --nginx-source-dir=./nginx-1.7.7

    touch checkpoints/passenger
    touch checkpoints/nginx
fi


# Create log directories
[ ! -d /opt/nginx/logs/ografy.io ] && sudo mkdir /opt/nginx/logs/ografy.io
[ ! -d /opt/nginx/logs/ografy.io/static ] && sudo mkdir /opt/nginx/logs/ografy.io/static
[ ! -d /opt/nginx/logs/ografy.io/www ] && sudo mkdir /opt/nginx/logs/ografy.io/www


# Create certificate directory structure
[ ! -d /security ] && sudo mkdir /security
[ ! -d /security/certs ] && sudo mkdir /security/certs
[ ! -d /security/certs/ografy.io ] && sudo mkdir /security/certs/ografy.io
[ ! -d /security/certs/ografy.io/static ] && sudo mkdir /security/certs/ografy.io/static
[ ! -d /security/certs/ografy.io/www ] && sudo mkdir /security/certs/ografy.io/www


if [ -f deploy.tar.gz ]
then
    rm -rf deploy
    tar -xzf deploy.tar.gz

    # Install nginx scripts and configurations
    sudo cp deploy/scripts/install/nginx /etc/init.d
    sudo chmod +x /etc/init.d/nginx

    if [ -f $"deploy/hosts/$1/conf/nginx/nginx.conf" ]
    then
        sudo cp deploy/hosts/$1/conf/nginx/nginx.conf /opt/nginx/conf
    else
        echo No nginx config found.
    fi

    if [ -d $"deploy/hosts/$1/certs" ]
    then
        sudo cp deploy/hosts/$1/certs/* /security/certs/ografy.io/static
        sudo cp deploy/hosts/$1/certs/* /security/certs/ografy.io/www
    else
        echo No certificates found.
    fi
fi
