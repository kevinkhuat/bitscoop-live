#!/bin/bash

cd ~/

# Create Python virtual environments
if [ ! -d ~/environments ]
then
    mkdir ~/environments
    cd ~/environments
    /usr/local/bin/virtualenv --no-site-packages ografy-3.4
    cd ..
fi


# FIXME: For now scp a tar'd copy of the local working Ografy repo into virtual machine.
[ ! -f ografy.tar.gz ] && echo File ografy.tar.gz not found. Aborting... && exit 1


# Extract Ografy tarball
[ ! -d ografy ] && tar -xzf ografy.tar.gz
# Create empty folders for logs and databases
[ ! -d ografy/databases ] && mkdir ografy/databases
[ ! -d ografy/logs ] && mkdir ografy/logs


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


# Install Ografy dependencies with pip and set up application
source ~/environments/ografy-3.4/bin/activate
pip install -r ~/sites/ografy.io/www/ografy/requirements/manual.txt
yes | python ~/sites/ografy.io/www/ografy/manage.py migrate
yes | python ~/sites/ografy.io/www/ografy/manage.py validate
yes yes | python ~/sites/ografy.io/www/ografy/manage.py collectstatic
deactivate


# Deploy Ografy project
[ -d sites ] && sudo rm -rf sites
mkdir sites
mkdir sites/ografy.io
mkdir sites/ografy.io/static
mkdir sites/ografy.io/static/public
mkdir sites/ografy.io/www
mkdir sites/ografy.io/www/public
mkdir sites/ografy.io/www/tmp
mv ografy/build/static/* sites/ografy.io/static/public
sudo rm -rf ografy/build
cp -r ografy sites/ografy.io/www
cp ografy/deploy/hosts/$1/web/passenger/passenger_wsgi.py sites/ografy.io/www


# Set the permissions on the created Ografy folder tree
chmod g+x,o+x .
chmod g+x,o+x sites
chmod g+x,o+x sites/ografy.io
chmod g+x,o+x sites/ografy.io/www
chmod g+x,o+x sites/ografy.io/www/passenger_wsgi.py
