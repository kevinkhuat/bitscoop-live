#!/bin/sh
# @authors Kyle Baran, Liam Broza
sudo cp nginx.repo /etc/yum.repos.d/
yes | sudo yum install nginx
sudo mkdir /etc/init.d/nginx
sudo cp -r nginx /etc/init.d/nginx/