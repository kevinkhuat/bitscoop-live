#!/bin/bash


WD=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
CUSR=ec2-user


usage() {
cat << EOF
usage: ${0} options

OPTIONS:
    -t    Host type. Can be \`production\` or \`virtual\`.

   [-s]  Django settings module to use. Overrides default associated with server type.
EOF
}


# Parse options.
while getopts ":hs:t:" OPTION; do
    case ${OPTION} in
        h)
            usage
            exit 0
            ;;
        s)
            SETTINGS=${OPTARG}
            ;;
        t)
            TYPE=${OPTARG}
            ;;
        ?)
            usage
            exit 1
            ;;
    esac
done


case ${TYPE} in
    production)
        SETTINGS=${SETTINGS:="ografy.settings.production"}
        ;;
    virtual)
        SETTINGS=${SETTINGS:="ografy.settings.virtual"}
        ;;
    *)
        echo "Invalid type: ${TYPE}"
        exit 1
        ;;
esac


# Install packages.
sudo yum install -y --disablerepo=* --enablerepo=ografy stunnel
sudo -u ${CUSR} ${WD}/../../scripts/installation/Python-3.4.2.sh install
sudo -u ${CUSR} ${WD}/../../scripts/installation/passenger-4.0.53.sh install
sudo -u ${CUSR} ${WD}/../../scripts/installation/ografy-0.2.0.sh install


# Set appropriate default permissions.
umask 022


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
