#!/bin/bash


WD=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )


# Install base packages.
sudo yum update -y
sudo yum install -y \
    bind \
    bind-utils \
    eject \
    man \
    nano \
    nc \
    net-tools \
    nfs-utils \
    nfs-utils-lib \
    ntp \
    ntpdate \
    ntp-doc \
    openssh-server \
    openssh-clients \
    vim \
    wget \
    yum-utils


umask 022
sudo cp -rv ${WD}/etc ${WD}/usr /


sudo mkdir -p /mnt/ografy
