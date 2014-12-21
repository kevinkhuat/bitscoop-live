#!/bin/bash


FLAG=/installed/redis-2.8.17


install() {
    # Install dependencies.
    sudo yum install -y gcc openssl-devel

    # Download source tarball if it doesn't already exist.
    [ ! -f redis-2.8.17.tar.gz ] && wget -P ${HOME} http://download.redis.io/releases/redis-2.8.17.tar.gz

    # Verify tarball checksum.
    SHA512=29515abd4437e03da20063a1831f0eb11ac65ba9d51cbfbb1987726102e3a55c76a3286b8c9a3bfbaf5290998fb5b662ef4aadbe0d131cd60824c8533e088441

    if [ ! -n "`openssl dgst -sha512 redis-2.8.17.tar.gz | grep ${SHA512}`" ]
    then
        echo "Invalid redis SHA512 checksum. Aborting..."
        exit 1
    fi

    # Extract source tarballs.
    [ ! -d ${HOME}/redis-2.8.17 ] && tar -xzf ${HOME}/redis-2.8.17.tar.gz -C ${HOME}


    # Perform installation.
    cd ${HOME}/redis-2.8.17
    cd deps
    make make hiredis lua jemalloc linenoise
    cd ..
    make

    sudo mkdir -p /opt/redis/bin
    sudo mkdir -p /opt/redis/conf

    sudo cp ${HOME}/redis-2.8.17/redis.conf /opt/redis/conf/redis.conf.default
    sudo cp ${HOME}/redis-2.8.17/sentinel.conf /opt/redis/conf

    sudo cp ${HOME}/redis-2.8.17/src/redis-benchmark /opt/redis/bin
    sudo cp ${HOME}/redis-2.8.17/src/redis-cli /opt/redis/bin
    sudo cp ${HOME}/redis-2.8.17/src/redis-server /opt/redis/bin
    sudo cp ${HOME}/redis-2.8.17/src/redis-check-aof /opt/redis/bin
    sudo cp ${HOME}/redis-2.8.17/src/redis-check-dump /opt/redis/bin


    # Create install checkpoint
    sudo mkdir -p `dirname ${FLAG}`
    sudo touch ${FLAG}
}


case ${1} in
    install)
        # Check to see if redis-2.8.17 is already installed.
        if [ -f ${FLAG} ]
        then
            echo "redis-2.8.17 already installed."
            exit 0
        fi

        install
        ;;
    uninstall)
        sudo rm -vf ${FLAG}
        echo "redis-2.8.17 uninstalled."
        ;;
    *)
        echo "Usage: ${0} {install|uninstall}"
        exit 1
        ;;
esac
