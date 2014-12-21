#!/bin/sh


SHA512=91326aa20ecc6a4b80ab0e98453e5b4f717eb2bbfedaed6aeaac9a26ada28c1c19e6f92d5a3d1397d9d28cdf27d27285f8d9f4431c6edb24093984265b885a9a


# Check to see if Python-3.4.2 is already installed.
[ -f /installed/mongo-2.6.4 ] && echo mongo-2.6.4 already installed. && exit 0


# Download source tarball if it doesn't already exist.
[ ! -f ${HOME}/mongodb-linux-x86_64-2.6.5.tgz ] && wget -P ${HOME} https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-2.6.5.tgz


# Verify tarball checksum.
[ ! -n "`openssl dgst -sha512 ${HOME}/mongodb-linux-x86_64-2.6.5.tgz | grep ${SHA512}`" ] && echo Invalid MongoDB SHA512 checksum. Aborting... && exit 1


# Extract source tarballs.
[ ! -d ${HOME}/mongodb-linux-x86_64-2.6.5 ] && tar -xzf ${HOME}/mongodb-linux-x86_64-2.6.5.tgz -C ${HOME}


# Perform installation.
sudo mkdir -p /opt/mongo/bin
sudo mkdir -p /opt/mongo/conf
sudo cp -r ${HOME}/mongodb-linux-x86_64-2.6.5/bin/* /opt/mongo/bin


# Create install checkpoint
sudo mkdir -p /installed
sudo touch /installed/mongo-2.6.4
