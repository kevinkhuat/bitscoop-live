#!/bin/bash


WD=`dirname ${BASH_SOURCE}`
source ${WD}/../parseargs.sh
source ${WD}/../baseline.sh


case ${TYPE} in
    production)
        echo "Using aws settings for web config."

        CUSR=ec2-user
        SETTINGS=${SETTINGS:="ografy.settings.production"}
        CUSR_HOME=`sudo su - ${CUSR} -c "echo ${HOME}"`
        ;;
    virtual)
        echo "Using virtual settings for web config."

        CUSR=ec2-user
        SETTINGS=${SETTINGS:="ografy.settings.virtual.local"}
        CUSR_HOME=`sudo su - ${CUSR} -c "echo ${HOME}"`
        ;;
esac


# Create log directory structure.
sudo mkdir -p /var/log/nginx/ografy.io/static
sudo mkdir -p /var/log/nginx/ografy.io/www


# Create certificate directory structure.
sudo mkdir -p /security/certs/ografy.io/static
sudo mkdir -p /security/certs/ografy.io/www


# Install packages from source.
sudo -u ${CUSR} ${WD}/../../scripts/installation/Python-3.4.2.sh install
sudo -u ${CUSR} ${WD}/../../scripts/installation/passenger-4.0.53.sh install


##################
# APPLY SETTINGS #
##################

case ${TYPE} in
    production)
        sudo cp -v ${WD}/conf/nginx.conf /opt/nginx/conf

        echo "SSL certificates have NOT been automatically installed."
        echo "These certificates must be manually deployed into production machines."
        ;;
    virtual)
        sudo cp -v ${WD}/conf/virtual/nginx.conf.virtual /opt/nginx/conf/nginx.conf

        sudo cp -v ${WD}/etc/ssl/certs/nginx.crt.virtual /security/certs/ografy.io/static/nginx.crt
        sudo cp -v ${WD}/etc/ssl/certs/nginx.key.virtual /security/certs/ografy.io/static/nginx.key
        sudo cp -v ${WD}/etc/ssl/certs/nginx.crt.virtual /security/certs/ografy.io/www/nginx.crt
        sudo cp -v ${WD}/etc/ssl/certs/nginx.key.virtual /security/certs/ografy.io/www/nginx.key
        ;;
esac


case ${PLATFORM} in
    ami)
        echo "Executing ami platform configuration."
        ;;
    centos)
        echo "Executing centos platform configuration."

        sudo -u ${CUSR} ${WD}/../../scripts/configuration/centos/firewalld.sh
        ;;
esac


# Set Django settings module environment variable.
echo "Setting environment variable DJANGO_SETTINGS_MODULE to \"${SETTINGS}\""
TMP=`mktemp`
echo "export DJANGO_SETTINGS_MODULE=\"${SETTINGS}\"" > ${TMP}
sudo cp ${TMP} /etc/profile.d/django.sh
sudo chmod 644 /etc/profile.d/django.sh
rm ${TMP}


#################
# DEPLOY OGRAFY #
#################

# Add new user ografy if it doesn't already exist.
if [ -z `getent passwd ografy` ]
then
    sudo adduser ografy
    sudo passwd -l ografy
fi

# Copy specific CUSR files to ografy user.
sudo cp ${CUSR_HOME}/ografy.tar.gz ${CUSR_HOME}/static.tar.gz ${WD}/../../scripts/installation/ografy-0.2.0.sh /home/ografy
sudo chown ografy:ografy /home/ografy/ografy.tar.gz /home/ografy/static.tar.gz /home/ografy/ografy-0.2.0.sh
sudo chmod +x /home/ografy/ografy-0.2.0.sh

# Install ografy package.
sudo su - ografy "/home/ografy/ografy-0.2.0.sh"

# Remove obsoleted files.
sudo rm /home/ografy/ografy.tar.gz /home/ografy/static.tar.gz /home/ografy/ografy-0.2.0.sh
