#!/bin/bash


# FIXME: For now scp a tar'd copy of the local working Ografy repo into virtual machine.
[ ! -f ografy.tar.gz ] && echo File ografy.tar.gz not found. Aborting... && exit 1


# Extract Ografy tarball
[ ! -d ografy ] && tar -xzf ografy.tar.gz
# Create empty folders for logs and databases
[ ! -d ografy/databases ] && mkdir ografy/databases
[ ! -d ografy/logs ] && mkdir ografy/logs


# Establish variables
case "$1" in
    production)
        MANAGE=ografy/manage_production.py
        echo Using production settings.
        ;;
    virtual)
        MANAGE=ografy/manage_virtual.py
        echo Using virtual settings.
        ;;
    *)
        echo $"Usage: $0 {production|virtual}"
        exit 2
        ;;
esac


# Create Python virtual environments
if [ ! -d environments ]
then
    mkdir environments
    cd environments
    /usr/local/bin/virtualenv --no-site-packages ografy-3.4
    cd ..
fi


# Install Ografy dependencies with pip and set up application
source environments/ografy-3.4/bin/activate
pip install -r ografy/requirements/manual.txt
yes | python $MANAGE migrate
yes | python $MANAGE validate
yes yes | python $MANAGE collectstatic
deactivate


# Deploy Ografy project
[ -d sites ] && rm -rf sites
mkdir sites
mkdir sites/ografy.io
mkdir sites/ografy.io/static
mkdir sites/ografy.io/static/public
mkdir sites/ografy.io/www
mkdir sites/ografy.io/www/public
mkdir sites/ografy.io/www/tmp
mv ografy/build/static/* sites/ografy.io/static/public
rm -rf ografy/build
cp -r ografy sites/ografy.io/www
cp deploy/hosts/$1/conf/passenger/passenger_wsgi.py sites/ografy.io/www


# Set the permissions on the created Ografy folder tree
chmod g+x,o+x .
chmod g+x,o+x sites
chmod g+x,o+x sites/ografy.io
chmod g+x,o+x sites/ografy.io/www
chmod g+x,o+x sites/ografy.io/www/passenger_wsgi.py