#!/bin/bash


# Install base packages.
sudo yum update -y
sudo yum install -y eject man nano net-tools nfs-utils nfs-utils-lib ntp ntpdate ntp-doc openssh-server openssh-clients package-cleanup vim wget yum-utils


# Set default values for variables should another script be calling this one.
CUSR=ec2-user
