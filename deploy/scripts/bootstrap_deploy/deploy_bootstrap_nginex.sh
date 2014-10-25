#!/bin/sh
# @authors Kyle Baran, Liam Broza
cd /
sudo cp ~/nginx.repo /etc/yum.repos.d/
yes | sudo yum install nginx

