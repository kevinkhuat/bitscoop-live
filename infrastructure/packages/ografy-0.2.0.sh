#!/bin/bash


# Establish variables
case "$1" in
    aws)
        echo Using aws settings for ografy.

        # Set environment variable for django
        export DJANGO_SETTINGS_MODULE='ografy.settings.production'

        ;;

    virtual)
        echo Using virtual settings for ografy.

        # Set environment variable for django
        export DJANGO_SETTINGS_MODULE='ografy.settings.virtual'

        ;;

    *)
        echo $"Usage: $0 {aws|virtual}"
        exit 2
        ;;

esac

if [ "$3" == "light" ]
then
    # Set environment variable for django
    export DJANGO_SETTINGS_MODULE='ografy.settings.light'
fi

# Create installed checkpoints folder.
[ ! -d /installed ] && sudo mkdir /installed && sudo chmod -R 777 /installed

# Create packages folder.
[ ! -d /packages ] && sudo mkdir /packages && sudo chmod -R 777 /packages


# Install Ografy
[ -f /installed/ografy-0.2.0 ] && [ "$2" != "force" ] && echo ografy-0.2.0 already installed. && exit 0

cd $HOME/

# Create Python virtual environments
if [ ! -d $HOME/environments ]
then
    mkdir $HOME/environments
    cd $HOME/environments
    /usr/local/bin/virtualenv --no-site-packages ografy-3.4
    cd ..
fi

[ ! -f $HOME/ografy.tar.gz ] && echo File ografy.tar.gz not found. Aborting... && exit 1


# Extract Ografy tarball
[ ! -d $HOME/ografy ] && tar -xzf ografy.tar.gz -C /$HOME
# Create empty folders for logs and databases
[ ! -d $HOME/ografy/databases ] && mkdir $HOME/ografy/databases
[ ! -d $HOME/ografy/logs ] && mkdir $HOME/ografy/logs


# Create log directories
[ ! -d /opt/nginx/logs/ografy.io ] && sudo mkdir /opt/nginx/logs/ografy.io
[ ! -d /opt/nginx/logs/ografy.io/static ] && sudo mkdir /opt/nginx/logs/ografy.io/static
[ ! -d /opt/nginx/logs/ografy.io/www ] && sudo mkdir /opt/nginx/logs/ografy.io/www


# Create certificate directory structure
[ ! -d /security ] && sudo mkdir /security && sudo chmod -R 777 /security
[ ! -d /security/certs ] && sudo mkdir /security/certs
[ ! -d /security/certs/ografy.io ] && sudo mkdir /security/certs/ografy.io
[ ! -d /security/certs/ografy.io/static ] && sudo mkdir /security/certs/ografy.io/static
[ ! -d /security/certs/ografy.io/www ] && sudo mkdir /security/certs/ografy.io/www


if [ -d $HOME/infrastructure ]
then

    # Install conf scripts and configurations
    sudo cp $HOME/infrastructure/scripts/init.d/nginx /etc/init.d
    sudo chmod +x /etc/init.d/nginx

    if [ -f $"$HOME/infrastructure/hosts/$1/conf/nginx.conf" ]
    then
        sudo cp $HOME/infrastructure/hosts/$1/conf/nginx.conf /opt/nginx/conf
    else
        echo No nginx config found.
    fi

    if [ -d $"$HOME/infrastructure/hosts/$1/certs" ]
    then
        sudo cp $HOME/infrastructure/hosts/$1/certs/* /security/certs/ografy.io/static
        sudo cp $HOME/infrastructure/hosts/$1/certs/* /security/certs/ografy.io/www
    else
        echo No certificates found.
    fi
fi


# Deploy Ografy project
[ -d $HOME/sites ] && sudo rm -rf sites
mkdir $HOME/sites
mkdir $HOME/sites/ografy.io
mkdir $HOME/sites/ografy.io/static
mkdir $HOME/sites/ografy.io/static/public
mkdir $HOME/sites/ografy.io/www
mkdir $HOME/sites/ografy.io/www/public
mkdir $HOME/sites/ografy.io/www/tmp
mv $HOME/ografy/build/static/* sites/ografy.io/static/public
sudo rm -rf $HOME/ografy/build
cp -r ografy sites/ografy.io/www
cp $HOME/sites/ografy.io/www/ografy/passenger_wsgi.py $HOME/sites/ografy.io/www


# Install Ografy dependencies with pip and set up application
source $HOME/environments/ografy-3.4/bin/activate
pip install -r $HOME/sites/ografy.io/www/ografy/requirements/manual.txt
yes | python $HOME/sites/ografy.io/www/ografy/manage.py migrate
yes | python $HOME/sites/ografy.io/www/ografy/manage.py validate
yes yes | python $HOME/sites/ografy.io/www/ografy/manage.py collectstatic
deactivate


# Set the permissions on the created Ografy folder tree
chmod g+x,o+x $HOME
chmod g+x,o+x $HOME/sites
chmod g+x,o+x $HOME/sites/ografy.io
chmod g+x,o+x $HOME/sites/ografy.io/www
chmod g+x,o+x $HOME/sites/ografy.io/www/passenger_wsgi.py

touch /installed/ografy-0.2.0
