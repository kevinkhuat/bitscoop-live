#!/bin/bash


[ ! -f ${HOME}/ografy.tar.gz ] && echo File ografy.tar.gz not found. Aborting... && exit 1

WWW=${HOME}/sites/ografy.io/www
STATIC=${HOME}/sites/ografy.io/static


# Backup existing databases if applicable
DATETIME=$(date +%Y-%m-%dT%T%z)
DATADIR=${HOME}/sites/ografy.io/www/ografy/databases
BKDIR=${HOME}/backups/${DATETIME}

# If database directory exists, then back up existing databases.
if [ `find sites/ografy.io/www/ografy/databases/ -type f | wc -l` -gt 0 ]
then
    mkdir -p ${BKDIR}
    # TODO: Is it a problem that we're moving the databases instead of copying?
    # Technically we shouldn't be running this script on a "live" server and we won't even be using sqlite, so it's probably a moot point.
    find ${DATADIR} -type f -exec mv {} ${BKDIR} \;
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


# If old databases were backed up, copy them back into the databases folder.
if [ -d ${BKDIR} ]
then
    cp ${BKDIR}/* ${DATADIR}
fi


# Create Python environment for ografy
if [ ! -f ${HOME}/environments/ografy-3.4/bin/activate ]
then
    cd ${HOME}/environments
    rm -rf ografy-3.4
    /usr/local/bin/virtualenv --no-site-packages ografy-3.4
    cd ..
fi


# Install Ografy dependencies with pip and set up application
source ${HOME}/environments/ografy-3.4/bin/activate
pip install -r ${WWW}/ografy/requirements/manual.txt
yes | python ${WWW}/ografy/manage.py makemigrations
yes | python ${WWW}/ografy/manage.py migrate
yes | python ${WWW}/ografy/manage.py validate
yes yes | python ${WWW}/ografy/manage.py collectstatic
deactivate


# Copy static files to serve location.
mv ${WWW}/ografy/build/static/* ${STATIC}/public
rm -rf ${WWW}/ografy/build


# Move passenger_wsgi file to appropriate location.
mv ${WWW}/ografy/passenger_wsgi.py ${WWW}


# Create Passenger restart file.
touch ${WWW}/tmp/restart.txt
ln -s ${WWW}/tmp/restart.txt ${HOME}/www.ografy.io


