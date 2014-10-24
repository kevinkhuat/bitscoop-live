#!/bin/sh
# This file bootstraps deployment from vagrantfile for dev test and production
# @authors Kyle Baran, Liam Broza
# curl http://nginx.org/download/nginx-1.7.6.tar.gz > nginx.tar.gz
# tar -zxvf nginx.tar.gz
# cd nginx-1.7.6/
sudo cd /
sudo cp nginx.repo /etc/yum.repos.d/
yes | sudo yum install nginx

