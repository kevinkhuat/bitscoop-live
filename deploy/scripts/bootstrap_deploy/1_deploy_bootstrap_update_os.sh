#!/bin/sh
# @authors Kyle Baran, Liam Broza
cd /
yes | sudo yum update
# Install necessary development tool compiler for C compiler and install Python 3 for production virtual environment
yes | sudo yum groupinstall -y development
