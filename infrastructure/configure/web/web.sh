#!/bin/bash


WD=`dirname ${BASH_SOURCE}`
source ${WD}/../parseargs.sh
source ${WD}/../baseline.sh


case ${TYPE} in
    production)
        SETTINGS=${SETTINGS:="ografy.settings.production"}
        ;;
    virtual)
        SETTINGS=${SETTINGS:="ografy.settings.virtual.local"}
        ;;
esac


# Install packages.
sudo yum install -y --disablerepo=* --enablerepo=ografy stunnel
sudo -u ${CUSR} ${WD}/../../scripts/installation/Python-3.4.2.sh install
sudo -u ${CUSR} ${WD}/../../scripts/installation/passenger-4.0.53.sh install


# Set appropriate default permissions.
umask 022


# Create log directory structure.
sudo mkdir -p /var/log/nginx/ografy.io/{static,www}


# Copy configuration files.
sudo cp -rv ${WD}/etc ${WD}/opt /


# Set Django settings module environment variable.
echo "Setting environment variable DJANGO_SETTINGS_MODULE to \"${SETTINGS}\""
TMP=`mktemp`
cat << EOF > ${TMP}
export DJANGO_SETTINGS_MODULE="${SETTINGS}"
EOF
sudo cp ${TMP} /etc/profile.d/django.sh
sudo chmod 644 /etc/profile.d/django.sh
rm ${TMP}


sudo chkconfig stunnel on
sudo service stunnel start

sudo chkconfig nginx on
sudo service nginx start
