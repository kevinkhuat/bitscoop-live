#!/bin/sh
# @authors Kyle Baran, Liam Broza
cd /
yes | sudo yum install ruby rubygem-rake
yes | sudo yum install libcurl-devel
yes | sudo yum install openssl-devel
yes | sudo yum install zlib-devel
yes | sudo yum install ruby-devel
yes | sudo /usr/bin/gem install rack
sudo mkdir /opt/passenger
cd /opt/passenger
sudo curl http://s3.amazonaws.com/phusion-passenger/releases/passenger-4.0.53.tar.gz > passenger.tar.gz
sudo tar xzvf passenger.tar.gz
cd passenger-4.0.53/
yes | sudo ./bin/passenger-install-nginx-module --languages python
export PATH="$PATH:/opt/nginx/sbin"
sudo cp -r /home/kbaran/ografy/deploy/scripts/bootstrap_deploy/nginx /etc/init.d/
sudo chmod +x /etc/init.d/nginx
sudo cp -r /home/kbaran/ografy/deploy/scripts/bootstrap_deploy/nginx.conf /opt/nginx/conf/
sudo mkdir /opt/nginx/html/public
sudo cp -r /home/kbaran/ografy/passenger_wsgi.py /opt/nginx/html/public/
sudo systemctl daemon-reload
sudo /etc/init.d/nginx start