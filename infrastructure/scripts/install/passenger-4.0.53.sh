#!/bin/bash


FLAG=/installed/passenger-4.0.53


install() {
    # Install dependencies.
    sudo yum install -y gcc-c++ libcurl-devel openssl-devel ruby rubygem-rake ruby-devel zlib-devel
    yes | sudo /usr/bin/gem install daemon_controller
    yes | sudo /usr/bin/gem install rack


    # Download source tarballs if they don't already exist.
    [ ! -f ${HOME}/passenger-4.0.53.tar.gz ] && wget -P ${HOME} https://s3.amazonaws.com/phusion-passenger/releases/passenger-4.0.53.tar.gz
    [ ! -f ${HOME}/nginx-1.7.7.tar.gz ] && wget -P ${HOME} http://nginx.org/download/nginx-1.7.7.tar.gz


    # Verify tarball checksums.
    SHA512=45919317c42da898783a22095fe75ed26f9142d227a25f5546f16861ce8c3ecfe2d804a845d389a00019df914cafd7625dc4e8fb31bc2f4ede5ecf41ce69c2a7
    if [ ! -n "`openssl dgst -sha512 ${HOME}/passenger-4.0.53.tar.gz | grep ${SHA512}`" ]
    then
        echo "Invalid Passenger SHA512 checksum. Aborting..."
        exit 1
    fi

    SHA512=3e8bf250e5f682a9a89cecd0b866b830735ebd5eb72ce760724d14b60296e9caa97abde7c79b46a6013ca013b9270a19aca55e0e43c8b8af123039f8341637d1
    if [ ! -n "`openssl dgst -sha512 ${HOME}/nginx-1.7.7.tar.gz | grep ${SHA512}`" ]
    then
        echo "Invalid nginx SHA512 checksum. Aborting..."
        exit 1
    fi


    # Extract source tarballs.
    [ ! -d ${HOME}/passenger-4.0.53 ] && tar -xzf ${HOME}/passenger-4.0.53.tar.gz -C ${HOME}
    [ ! -d ${HOME}/nginx-1.7.7 ] && tar -xzf ${HOME}/nginx-1.7.7.tar.gz -C ${HOME}


    # Perform installation.
    sudo mkdir -p /opt/passenger
    sudo cp -r ${HOME}/passenger-4.0.53/* /opt/passenger
    sudo /opt/passenger/bin/passenger-install-nginx-module --auto --languages python --nginx-source-dir=./nginx-1.7.7


    # Create install checkpoints
    sudo mkdir -p `dirname ${FLAG}`
    sudo touch ${FLAG}
}


case ${1} in
    install)
        # Check to see if passenger-4.0.53 with nginx-1.7.7 is already installed.
        if [ -f ${FLAG} ]
        then
            echo "passenger-4.0.53 with nginx-1.7.7 already installed."
            exit 0
        fi

        install
        ;;
    uninstall)
        sudo rm -f ${FLAG}
        echo "passenger-4.0.53 uninstalled."
        ;;
    *)
        echo "Usage: ${0} {install|uninstall}"
        exit 1
        ;;
esac
