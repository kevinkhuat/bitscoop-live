#!/bin/bash
# @authors Kyle Baran, Liam Broza


# Establish variables
case "$1" in
    aws)
        echo Using aws settings.
        ;;
    virtual)
        echo Using virtual settings.
        ;;
    *)
        echo $"Usage: $0 {aws|virtual}"
        exit 2
        ;;
esac


# Create Python virtual environments
if [ ! -d ~/environments ]
then
    mkdir ~/environments
    cd ~/environments
    /usr/local/bin/virtualenv --no-site-packages ografy-3.4
    cd ..
fi


# Configure Python install, build binaries from source, and install
if [ ! -f ~/checkpoints/python ]
then

    cd ~/packages

    [ -d Python-3.4.2 ] && rm -rf Python-3.4.2

    # Download source tarballs and signatures
    [ ! -f Python-3.4.2.tgz ] && wget https://www.python.org/ftp/python/3.4.2/Python-3.4.2.tgz

    tar -xzf Python-3.4.2.tgz
    cd Python-3.4.2
    # Configure install with the `with-ensurepip` flag set to install pip with Python (works with Python 3.4+)
    ./configure --with-ensurepip=install
    make
    sudo make altinstall
    # Ensure pip package manager is up to date
    sudo /usr/local/bin/pip3.4 install pip --upgrade
    # Install virtualenv to manage virtual Python environments
    sudo /usr/local/bin/pip3.4 install virtualenv

    cd ~/

    touch ~/checkpoints/python
fi
