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
        echo "Invalid type: ${TYPE}"
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
        SETTINGS=${SETTINGS:="ografy.settings.virtual"}
        CUSR_HOME=`sudo su - ${CUSR} -c "echo ${HOME}"`
        ;;
esac


# Create log directory structure.
sudo mkdir -p /var/log/mongo


####################
# INSTALL PACKAGES #
####################

# "Uninstall" relevant packages if force-related options are specified.
if [ ${FORCE:+x} ]
then
    echo "Forcing reinstallation of packages."

    sudo rm -f /installed/mongodb-2.6.4

    if [ ${REBUILD:+x} ]
    then
        echo "Forcing a fresh rebuild of packages."

        sudo rm -rf ${CUSR_HOME}/mongodb-linux-x86_64-2.6.5
    fi
fi

# Install packages.
sudo -u ${CUSR} $HOME/infrastructure/packages/mongodb-2.6.4.sh


##################
# APPLY SETTINGS #
##################

case ${TYPE} in
    production)
        sudo cp ${CUSR_HOME}/infrastructure/hosts/production/conf/mongod.conf /opt/mongo/conf
        ;;
    virtual)
        sudo cp ${CUSR_HOME}/infrastructure/hosts/virtual/conf/mongod.conf /opt/mongo/conf
        ;;
esac


case ${PLATFORM} in
    ami)
        echo "Executing ami platform configuration."
        ;;
    centos)
        echo "Executing centos platform configuration."

        ${CUSR_HOME}/infrastructure/platforms/centos/firewalld.sh
        ;;
esac


################
# CREATE USERS #
################

# Add new user mongod if it doesn't already exist.
if [ -z `getent passwd mongod` ]
then
    sudo useradd -d /var/lib/mongo mongod
    sudo passwd -l mongod
fi


###################
# INSTALL SCRIPTS #
###################

# Copy daemon scripts
sudo cp ${CUSR_HOME}/infrastructure/scripts/init.d/mongod /etc/init.d
sudo chmod +x /etc/init.d/mongod

# Start daemons.
sudo systemctl daemon-reload
sudo service mongod start
