#!/bin/bash


SHA512=29515abd4437e03da20063a1831f0eb11ac65ba9d51cbfbb1987726102e3a55c76a3286b8c9a3bfbaf5290998fb5b662ef4aadbe0d131cd60824c8533e088441


# Check to see if redis-2.8.17 is already installed.
[ -f /installed/redis-2.8.17 ] && [ "${1}" != "force" ] && echo redis-2.8.17 already installed. && exit 0


# Download source tarball if it doesn't already exist.
[ ! -f redis-2.8.17.tar.gz ] && wget -P ${HOME} http://download.redis.io/releases/redis-2.8.17.tar.gz


# Verify tarball checksum.
[ ! -n "`openssl dgst -sha512 redis-2.8.17.tar.gz | grep ${SHA512}`" ] && echo Invalid redis SHA512 checksum. Aborting... && exit 1


# Extract source tarballs.
[ ! -d ${HOME}/redis-2.8.17 ] && tar -xzf ${HOME}/redis-2.8.17.tar.gz -C ${HOME}


# Perform installation.
cd ${HOME}/redis-2.8.17
# Configure install with the `with-ensurepip` flag set to install pip with Python (works with Python 3.4+)
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
sudo mkdir -p /installed
sudo touch /installed/redis-2.8.17
