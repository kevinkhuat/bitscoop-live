#!/bin/sh
# @authors Kyle Baran, Liam Broza
sudo cp nginx.repo /etc/yum.repos.d/
yes | sudo yum install nginx
