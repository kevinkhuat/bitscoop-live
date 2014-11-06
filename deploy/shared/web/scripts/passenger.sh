#!/bin/bash
# @authors Kyle Baran, Liam Broza


# Establish variables
case "$1" in
    aws)
        echo Using aws settings.
        ;;
    virtual)
        echo Using virtual settings.
        ;;
    *)
        echo $"Usage: $0 {aws|virtual}"
        exit 2
        ;;
esac

# Download source tarballs and signatures
[ ! -f passenger-4.0.53.tar.gz ] && wget https://s3.amazonaws.com/phusion-passenger/releases/passenger-4.0.53.tar.gz
[ ! -f nginx-1.7.7.tar.gz ] && wget http://nginx.org/download/nginx-1.7.7.tar.gz

# Install Passenger w/ nginx
if [ ! -f ~/checkpoints/passenger ]
then

    cd ~/packages

    [ -d passenger-4.0.53 ] && rm -rf passenger-4.0.53
    [ -d nginx-1.7.7 ] && rm -rf nginx-1.7.7

    tar -xzf passenger-4.0.53.tar.gz
    tar -xzf nginx-1.7.7.tar.gz

    [ ! -d /opt/passenger ] && sudo mkdir /opt/passenger
    sudo cp -r passenger-4.0.53/* /opt/passenger
    sudo /opt/passenger/bin/passenger-install-nginx-module --auto --languages python --nginx-source-dir=./nginx-1.7.7

    touch ~/checkpoints/passenger
    touch ~/checkpoints/nginx

fi

cd ~/

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
    sudo cp deploy/shared/web/install/nginx /etc/init.d
    sudo chmod +x /etc/init.d/nginx

    if [ -f $"deploy/hosts/$1/web/nginx/nginx.conf" ]
    then
        sudo cp deploy/hosts/$1/web/nginx/nginx.conf /opt/nginx/conf
    else
        echo No nginx config found.
    fi

    if [ -d $"deploy/hosts/$1/web/certs" ]
    then
        sudo cp deploy/hosts/$1/web/certs/* /security/certs/ografy.io/static
        sudo cp deploy/hosts/$1/web/certs/* /security/certs/ografy.io/www
    else
        echo No certificates found.
    fi
fi
