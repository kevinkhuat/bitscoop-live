#!/bin/sh
# @authors Kyle Baran, Liam Broza
# $1 argument is github username:password

# Update OS
sudo yum update -y

# Install necessary development tools
#yes | sudo yum groupinstall -y development

# Python dependancies
sudo yum install -y wget
sudo yum install -y gcc
sudo yum install -y openssl-devel

# Ografy dependancies
sudo yum install -y sqlite-devel
sudo yum install -y git

# Passenger dependances
sudo yum install -y ruby
sudo yum install -y ruby rubygem-rake
sudo yum install -y ruby-devel
sudo /usr/bin/gem install -y rack
sudo /usr/bin/gem install -y daemon_controller
sudo yum install -y libcurl-devel
sudo yum install -y zlib-devel
sudo yum install -y gcc-c++

# Get ografy code and put it in the home dir
mkdir ~/sites
mkdir ~/sites/ografy.io
mkdir ~/sites/ografy.io/www
# sudo curl -L -u $1 https://github.com/sjberry/ografy/archive/v0.1.0.tar.gz > ografy.tar.gz
tar -xzf ~/ografy.tar.gz
cd ografy
cp -r * ~/sites/ografy.io/www/

# install Python
yes | sudo yum install sqlite-devel
wget https://www.python.org/ftp/python/3.4.2/Python-3.4.2.tgz
wget https://www.python.org/ftp/python/3.4.2/Python-3.4.2.tgz.asc
gpg --recv-keys 6A45C816 36580288 7D9DC8D2 18ADD4FF A4135B38 A74B06BF EA5BBD71 ED9D77D5 E6DF025C 6F5E1540 F73C700D
# TODO: Fail on bad condition
gpg --verify Python-3.4.2.tgz.asc
tar -xzf Python-3.4.2.tgz
cd ~/Python-3.4.2
yes | sudo ./configure
yes | sudo make && sudo make altinstall
export PATH="$PATH:/usr/local/bin/python3.4"
wget https://bootstrap.pypa.io/ez_setup.py
sudo /usr/local/bin/python3.4 ez_setup.py
sudo /usr/local/bin/easy_install pip
yes | sudo /usr/local/bin/pip install virtualenv
cd ~/
/usr/local/bin/virtualenv ografy_env
source ~/ografy_env/bin/activate

# Prep ografy project
cd ~/sites/ografy.io/www
yes | ~/ografy_env/bin/pip  install -r requirements/manual.txt
yes | python manage.py migrate
yes | python manage.py validate
yes yes | python manage.py collectstatic

# Prep SSL by manually executing these commands on host machine and copying in the certs to www root
# TODO: Make programatic / add real signed certs
# sudo openssl genrsa -des3 -out server.key 1024
# sudo openssl req -new -key server.key -out server.csr
# sudo cp server.key server.key.org
# sudo openssl rsa -in server.key.org -out server.key
# sudo openssl x509 -req -days 365 -in server.csr -signkey server.key -out server.crt
# TODO: Copy certs to correct dir

# install passenger
cd ~/
sudo mkdir /opt/passenger
wget http://s3.amazonaws.com/phusion-passenger/releases/passenger-4.0.53.tar.gz
tar -xzvf passenger-4.0.53.tar.gz
cd passenger-4.0.53
yes | sudo ./bin/passenger-install-nginx-module --languages python
export PATH="$PATH:/opt/nginx/sbin"
sudo cp -r ~/sites/ografy.io/www/deploy/scripts/files/nginx /etc/init.d/
sudo chmod +x /etc/init.d/nginx
sudo mkdir /opt/nginx/conf
sudo cp -r ~/sites/ografy.io/www/deploy/scripts/files/nginx.conf /opt/nginx/conf/
sudo systemctl daemon-reload
sudo /etc/init.d/nginx start
