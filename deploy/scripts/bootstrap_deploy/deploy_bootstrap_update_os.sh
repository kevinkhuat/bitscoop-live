#!/bin/sh
# This file bootstraps deployment from vagrantfile for dev test and production
# @authors Kyle Baran, Liam Broza
#ToDo fix this for production. Don't run update each time because it takes forever.
sudo cd /
yes | sudo yum update
# Install necessary development tool compiler for C compiler and install Python 3 for production virtual environment
yes | sudo yum groupinstall -y development
