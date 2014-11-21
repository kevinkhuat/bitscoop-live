#!/bin/bash


usage() {
cat << EOF
usage: ${0} options

OPTIONS:
    -t    Host type. Can be \`production\` or \`virtual\`.
    -p    Platform. Can be \`ami\` or \`centos\`.

   [-f]  Force reinstallation of packages.
   [-r]  Full source rebuild of packages. Sets -f force flag to TRUE.
   [-s]  Django settings module to use. Overrides default associated with server type.
EOF
}


###################
# PARSE ARGUMENTS #
###################

while getopts ":hfp:rs:t:" OPTION; do
    case ${OPTION} in
        h)
            usage
            exit 0
            ;;
        f)
            FORCE=1
            ;;
        p)
            PLATFORM=${OPTARG}
            ;;
        r)
            FORCE=1
            REBUILD=1
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
        ;;
    virtual)
        ;;
    *)
        echo "Invalid type: ${TYPE+x}"
        exit 1
        ;;
esac


case ${PLATFORM} in
    ami)
        ;;
    centos)
        ;;
    *)
        echo "Invalid platform: ${PLATFORM}"
        exit 1
        ;;
esac


#####################
# BEGIN MAIN SCRIPT #
#####################

# Create log directory structure.
sudo mkdir -p /var/log/nginx/ografy.io/static
sudo mkdir -p /var/log/nginx/ografy.io/www


# Create certificate directory structure.
sudo mkdir -p /security/certs/ografy.io/static
sudo mkdir -p /security/certs/ografy.io/www


case ${TYPE} in
    production)
        echo "Using aws settings for web config."

        CUSR=ec2-user
        SETTINGS=${SETTINGS:="ografy.settings.production"}
        CUSR_HOME=`sudo su - ${CUSR} -c "echo ${HOME}"`

        sudo cp ${CUSR_HOME}/infrastructure/hosts/production/conf/nginx.conf /opt/nginx/conf

        echo "SSL certificates have NOT been automatically installed."
        echo "These certificates must be manually deployed into production machines."
        ;;
    virtual)
        echo "Using virtual settings for web config."

        CUSR=ec2-user
        SETTINGS=${SETTINGS:="ografy.settings.virtual"}
        CUSR_HOME=`sudo su - ${CUSR} -c "echo ${HOME}"`

        sudo cp ${CUSR_HOME}/infrastructure/hosts/virtual/conf/nginx.conf /opt/nginx/conf
        sudo cp ${CUSR_HOME}/infrastructure/hosts/virtual/certs/* /security/certs/ografy.io/static
        sudo cp ${CUSR_HOME}/infrastructure/hosts/virtual/certs/* /security/certs/ografy.io/www
        ;;
esac


case ${PLATFORM} in
    ami)
        echo "Executing ami platform configuration."
        ;;
    centos)
        echo "Executing centos platform configuration."

        ${CUSR_HOME}/infrastructure/platforms/centos/firewall.sh
        ;;
esac


# Set Django settings module environment variable.
echo "Setting environment variable DJANGO_SETTINGS_MODULE to \"${SETTINGS}\""
TMP=`mktemp`
echo "export DJANGO_SETTINGS_MODULE=\"${SETTINGS}\"" > ${TMP}
sudo cp ${TMP} /etc/profile.d/django.sh
rm ${TMP}


####################
# Install Packages #
####################

# "Uninstall" relevant packages if force-related options are specified.
if [ ${FORCE:+x} ]
then
    echo "Forcing reinstallation of packages."

    [ -f /installed/Python-3.4.2 ] && sudo rm /installed/Python-3.4.2
    [ -f /installed/passenger-4.0.53 ] && sudo rm /installed/passenger-4.0.53
    [ -f /installed/nginx-1.7.7 ] && sudo rm /installed/nginx-1.7.7

    if [ ${REBUILD:+x} ]
    then
        echo "Forcing a fresh rebuild of packages."

        [ -f ${CUSR_HOME}/Python-3.4.2 ] && sudo rm -rf ${CUSR_HOME}/Python-3.4.2
        [ -f ${CUSR_HOME}/passenger-4.0.53 ] && sudo rm -rf ${CUSR_HOME}/passenger-4.0.53
        [ -f ${CUSR_HOME}/nginx-1.7.7 ] && sudo rm -rf ${CUSR_HOME}/nginx-1.7.7
    fi
fi

# Install packages from source.
sudo -u ${CUSR} $HOME/infrastructure/packages/Python-3.4.2.sh
sudo -u ${CUSR} $HOME/infrastructure/packages/passenger-4.0.53.sh


#################
# Deploy Ografy #
#################

# Add new user ografy if it doesn't already exist.
[ -z `getent passwd ografy` ] && sudo adduser ografy

# Copy specific CUSR files to ografy user.
sudo cp ${CUSR_HOME}/ografy.tar.gz /home/ografy
sudo chown ografy:ografy /home/ografy/ografy.tar.gz

sudo cp ${CUSR_HOME}/infrastructure/packages/ografy-0.2.0.sh /home/ografy
sudo chown ografy:ografy /home/ografy/ografy-0.2.0.sh
sudo chmod +x /home/ografy/ografy-0.2.0.sh

# Install ografy package.
sudo su - ografy "/home/ografy/ografy-0.2.0.sh"


###################
# Install Scripts #
###################

# Copy daemon scripts
sudo cp ${CUSR_HOME}/infrastructure/scripts/init.d/nginx /etc/init.d
sudo chmod +x /etc/init.d/nginx

# Start daemons.
#sudo service nginx start
