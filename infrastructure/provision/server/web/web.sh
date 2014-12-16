#!/bin/bash


SOURCE_DIR=`dirname ${BASH_SOURCE}`
source ${SOURCE_DIR}/../../common/parseargs.sh
source ${SOURCE_DIR}/../../common/baseline.sh


case ${TYPE} in
    production)
        echo "Using aws settings for web config."

        CUSR=ec2-user
        SETTINGS=${SETTINGS:="ografy.settings.production.sqlite"}
        CUSR_HOME=`sudo su - ${CUSR} -c "echo ${HOME}"`
        ;;
    virtual)
        echo "Using virtual settings for web config."

        CUSR=ec2-user
        SETTINGS=${SETTINGS:="ografy.settings.virtual.sqlite"}
        CUSR_HOME=`sudo su - ${CUSR} -c "echo ${HOME}"`
        ;;
esac


# Create log directory structure.
sudo mkdir -p /var/log/nginx/ografy.io/static
sudo mkdir -p /var/log/nginx/ografy.io/www


# Create certificate directory structure.
sudo mkdir -p /security/certs/ografy.io/static
sudo mkdir -p /security/certs/ografy.io/www


####################
# INSTALL PACKAGES #
####################

# "Uninstall" relevant packages if force-related options are specified.
if [ ${FORCE:+x} ]
then
    echo "Forcing reinstallation of packages."

    sudo -u ${CUSR} ${CUSR_HOME}/infrastructure/scripts/install/Python-3.4.2.sh uninstall
    sudo -u ${CUSR} ${CUSR_HOME}/infrastructure/scripts/install/passenger-4.0.53.sh uninstall
fi

# Install packages from source.
sudo -u ${CUSR} ${CUSR_HOME}/infrastructure/scripts/install/Python-3.4.2.sh install
sudo -u ${CUSR} ${CUSR_HOME}/infrastructure/scripts/install/passenger-4.0.53.sh install


##################
# APPLY SETTINGS #
##################

case ${TYPE} in
    production)
        sudo cp -v ${SOURCE_DIR}/conf/production/nginx.conf /opt/nginx/conf

        echo "SSL certificates have NOT been automatically installed."
        echo "These certificates must be manually deployed into production machines."
        ;;
    virtual)
        sudo cp -v ${SOURCE_DIR}/conf/virtual/nginx.conf /opt/nginx/conf

        sudo cp -v ${CUSR_HOME}/infrastructure/certs/* /security/certs/ografy.io/static
        sudo cp -v ${CUSR_HOME}/infrastructure/certs/* /security/certs/ografy.io/www
        ;;
esac


case ${PLATFORM} in
    ami)
        echo "Executing ami platform configuration."
        ;;
    centos)
        echo "Executing centos platform configuration."

        sudo -u ${CUSR} ${CUSR_HOME}/infrastructure/scripts/config/centos/firewalld.sh
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
sudo cp ${CUSR_HOME}/ografy.tar.gz ${CUSR_HOME}/static.tar.gz ${CUSR_HOME}/infrastructure/scripts/install/ografy-0.2.0.sh /home/ografy
sudo chown ografy:ografy /home/ografy/ografy.tar.gz /home/ografy/static.tar.gz /home/ografy/ografy-0.2.0.sh
sudo chmod +x /home/ografy/ografy-0.2.0.sh

# Install ografy package.
sudo su - ografy "/home/ografy/ografy-0.2.0.sh"

# Remove obsoleted files.
sudo rm /home/ografy/ografy.tar.gz /home/ografy/static.tar.gz /home/ografy/ografy-0.2.0.sh


###################
# INSTALL SCRIPTS #
###################

# Copy daemon scripts
sudo cp ${SOURCE_DIR}/init.d/nginx /etc/init.d
sudo chmod +x /etc/init.d/nginx

# Start daemons.
sudo systemctl daemon-reload
sudo service nginx start
