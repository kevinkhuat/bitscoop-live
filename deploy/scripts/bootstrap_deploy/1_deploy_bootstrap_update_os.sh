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