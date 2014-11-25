#!/bin/bash


SHA512_PASSENGER=45919317c42da898783a22095fe75ed26f9142d227a25f5546f16861ce8c3ecfe2d804a845d389a00019df914cafd7625dc4e8fb31bc2f4ede5ecf41ce69c2a7
SHA512_NGINX=3e8bf250e5f682a9a89cecd0b866b830735ebd5eb72ce760724d14b60296e9caa97abde7c79b46a6013ca013b9270a19aca55e0e43c8b8af123039f8341637d1


# Check to see if passenger-4.0.53 with nginx-1.7.7 is already installed.
[ -f /installed/passenger-4.0.53 ] && echo passenger-4.0.53 with nginx-1.7.7 already installed. && exit 0


# Download source tarballs if they don't already exist.
[ ! -f ${HOME}/passenger-4.0.53.tar.gz ] && wget -P ${HOME} https://s3.amazonaws.com/phusion-passenger/releases/passenger-4.0.53.tar.gz
[ ! -f ${HOME}/nginx-1.7.7.tar.gz ] && wget -P ${HOME} http://nginx.org/download/nginx-1.7.7.tar.gz


# Verify tarball checksums.
[ ! -n "`openssl dgst -sha512 ${HOME}/passenger-4.0.53.tar.gz | grep ${SHA512_PASSENGER}`" ] && echo Invalid Passenger SHA512 checksum. Aborting... && exit 1
[ ! -n "`openssl dgst -sha512 ${HOME}/nginx-1.7.7.tar.gz | grep ${SHA512_NGINX}`" ] && echo Invalid nginx SHA512 checksum. Aborting... && exit 1


# Extract source tarballs.
[ ! -d ${HOME}/passenger-4.0.53 ] && tar -xzf ${HOME}/passenger-4.0.53.tar.gz -C ${HOME}
[ ! -d ${HOME}/nginx-1.7.7 ] && tar -xzf ${HOME}/nginx-1.7.7.tar.gz -C ${HOME}


# Perform installation.
sudo mkdir -p /opt/passenger
sudo cp -r ${HOME}/passenger-4.0.53/* /opt/passenger
sudo /opt/passenger/bin/passenger-install-nginx-module --auto --languages python --nginx-source-dir=./nginx-1.7.7


# Create install checkpoints
sudo mkdir -p /installed
sudo touch /installed/passenger-4.0.53
sudo touch /installed/nginx-1.7.7
