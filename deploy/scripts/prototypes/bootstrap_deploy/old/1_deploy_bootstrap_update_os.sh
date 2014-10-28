#!/bin/sh
# @authors Kyle Baran, Liam Broza

yes | sudo yum update
# Install necessary development tool compiler for C compiler and install Python 3 for production virtual environment
#yes | sudo yum groupinstall -y development
yes | sudo yum install wget
yes | sudo yum install gcc
yes | sudo yum install openssl-devel
yes | sudo yum install zlib-devel
yes | sudo yum install sqlite-devel
yes | sudo yum install git
mkdir ~/sites
mkdir ~/sites/ografy.io
mkdir ~/sites/ografy.io/www
# sudo curl -L -u mrhegemon:p https://github.com/sjberry/ografy/archive/v0.1.0.tar.gz > ografy.tar.gz
tar -xzf ografy.tar.gz ~/sites/ografy.io/www
cd ~/sites/ografy.io/www/deploy/scripts/bootstrap_deploy
sh 2_deploy_bootstrap_passenger.sh

