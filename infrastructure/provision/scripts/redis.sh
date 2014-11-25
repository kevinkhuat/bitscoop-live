#!/bin/bash


usage() {
cat << EOF
usage: ${0} options

OPTIONS:
    -t    Host type. Can be \`production\` or \`virtual\`.
    -p    Platform. Can be \`ami\` or \`centos\`.

   [-f]  Force reinstallation of packages.
   [-r]  Full source rebuild of packages. Sets -f force flag to TRUE.
EOF
}


###################
# PARSE ARGUMENTS #
###################

while getopts ":hfp:rt:" OPTION; do
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
        echo "Using production settings for redis config."

        CUSR=ec2-user
        CUSR_HOME=`sudo su - ${CUSR} -c "echo ${HOME}"`
        ;;
    virtual)
        echo "Using virtual settings for redis config."

        CUSR=ec2-user
        CUSR_HOME=`sudo su - ${CUSR} -c "echo ${HOME}"`
        ;;
esac

# Create log directory structure.
sudo mkdir -p /var/log/redis


####################
# INSTALL PACKAGES #
####################

# "Uninstall" relevant packages if force-related options are specified.
if [ ${FORCE:+x} ]
then
    echo "Forcing reinstallation of packages."

    [ -f /installed/redis-2.8.17 ] && sudo rm /installed/redis-2.8.17

    if [ ${REBUILD:+x} ]
    then
        echo "Forcing a fresh rebuild of packages."

        [ -d ${CUSR_HOME}/redis-2.8.17 ] && sudo rm -rf ${CUSR_HOME}/redis-2.8.17
    fi
fi

# Install packages from source.
sudo -u ${CUSR} $HOME/infrastructure/packages/redis-2.8.17.sh


##################
# APPLY SETTINGS #
##################

case ${TYPE} in
    production)
        sudo cp ${CUSR_HOME}/infrastructure/hosts/production/conf/redis.conf /opt/redis/conf
        ;;
    virtual)
        sudo cp ${CUSR_HOME}/infrastructure/hosts/virtual/conf/redis.conf /opt/redis/conf
        ;;
esac


case ${PLATFORM} in
    ami)
        echo "Executing ami platform configuration."
        ;;
    centos)
        echo "Executing centos platform configuration."
        ;;
esac


###################
# INSTALL SCRIPTS #
###################

# Copy daemon scripts
sudo cp ${CUSR_HOME}/infrastructure/scripts/init.d/redis /etc/init.d
sudo chmod +x /etc/init.d/redis

# Start daemons.
sudo systemctl daemon-reload
sudo service redis start
