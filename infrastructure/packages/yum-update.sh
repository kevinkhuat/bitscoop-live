#!/bin/bash
# @authors Kyle Baran, Liam Broza

# Update OS
sudo yum update -y


# Install package dependencies

# Needed to decompress some pip dependencies.
sudo yum install -y bzip2-devel
# Compiles C packages (e.g. Python) from source
sudo yum install -y gcc
# Compiles C++ (e.g. Passenger) from source
sudo yum install -y gcc-c++
# Git clone Ografy repository
sudo yum install -y git
# Passenger bindings
sudo yum install -y libcurl-devel
# Needed to sync time with global time
sudo yum install -y ntp ntpdate ntp-doc
# Required for the installation of `pip` with Python make and SSL signing
# CentOS equivalent of `libssl-devel`
sudo yum install -y openssl-devel
# Passenger runtime and build dependency
sudo yum install -y ruby
# Required to install gem requirements
sudo yum install -y rubygem-rake
# Bindings required for building Passenger
sudo yum install -y ruby-devel
# Required for compiling Python sqlite3 bindings
sudo yum install -y sqlite-devel
# Used to download source dependencies
sudo yum install -y wget
# Passenger bindings
sudo yum install -y zlib-devel
# PostgreSQL tools
sudo yum install -y postgresql-devel

# Additional Passenger gem dependances
[ ! -n "`gem list | grep daemon_controller`" ] && yes | sudo /usr/bin/gem install daemon_controller
[ ! -n "`gem list | grep rack`" ] && yes | sudo /usr/bin/gem install rack
