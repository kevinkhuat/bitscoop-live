#!/bin/bash


[ ! -f ${HOME}/ografy.tar.gz ] && echo File ografy.tar.gz not found. Aborting... && exit 1

WWW=${HOME}/sites/ografy.io/www
STATIC=${HOME}/sites/ografy.io/static


# Backup existing databases if applicable
DATETIME=$(date +%Y-%m-%dT%T%z)
DATADIR=${HOME}/sites/ografy.io/www/ografy/databases
BKDIR=${HOME}/backups/${DATETIME}

if [ -d ${DATADIR} ]
then
    mkdir -p ${BKDIR}
    find ${HOME}/sites/ografy.io/www/ografy/databases -type f -exec cp {} ${BKDIR} \;
fi


# Delete existing deployment.
rm -rf ${WWW}
rm -rf ${STATIC}


# Create new subdomain folders.
mkdir -p ${WWW}/public
mkdir -p ${WWW}/tmp
mkdir -p ${STATIC}/public


# Extract source tarball.
# TODO: Find out why this is giving a permission denied error when run as ec2-user through `sudo -u ografy`
tar -xzf ografy.tar.gz -C ${WWW} --no-same-owner


# Create empty folders for Python environments, Django logs, and Django databases.
mkdir -p ${HOME}/environments
mkdir -p ${WWW}/ografy/databases
mkdir -p ${WWW}/ografy/logs


# Create Python environment for ografy
if [ ! -f ${HOME}/environments/ografy-3.4/bin/activate ]
then
    cd ${HOME}/environments
    /usr/local/bin/virtualenv --no-site-packages ografy-3.4
    cd ..
fi


# Install Ografy dependencies with pip and set up application
source ${HOME}/environments/ografy-3.4/bin/activate
pip install -r ${WWW}/ografy/requirements/manual.txt
yes | python ${WWW}/ografy/manage.py migrate
yes | python ${WWW}/ografy/manage.py validate
yes yes | python ${WWW}/ografy/manage.py collectstatic
deactivate


mv ${WWW}/ografy/build/static/* ${STATIC}/public
rm -rf ${WWW}/ografy/build
mv ${WWW}/ografy/passenger_wsgi.py ${WWW}


touch ${WWW}/tmp/restart.txt


# Set the permissions on the created Ografy folder tree
#chmod g+x,o+x ${HOME}
#chmod g+x,o+x ${HOME}/sites
#chmod g+x,o+x ${HOME}/sites/ografy.io
#chmod g+x,o+x ${HOME}/sites/ografy.io/www
#chmod g+x,o+x ${HOME}/sites/ografy.io/www/passenger_wsgi.py
