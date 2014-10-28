#!/bin/sh
# @authors Kyle Baran, Liam Broza

# Update OS
yes | sudo yum update

# Install necessary development tools
#yes | sudo yum groupinstall -y development
yes | sudo yum install wget
yes | sudo yum install gcc
yes | sudo yum install openssl-devel
yes | sudo yum install zlib-devel
yes | sudo yum install sqlite-devel
yes | sudo yum install libcurl-devel
yes | sudo yum install git

# Get ografy code and put it in the home dir
mkdir ~/sites
mkdir ~/sites/ografy.io
mkdir ~/sites/ografy.io/www
# sudo curl -L -u mrhegemon:p https://github.com/sjberry/ografy/archive/v0.1.0.tar.gz > ografy.tar.gz
tar -xzf ografy.tar.gz ~/sites/ografy.io/www

# install Python
yes | sudo yum install sqlite-devel
wget https://www.python.org/ftp/python/3.4.2/Python-3.4.2.tgz
wget https://www.python.org/ftp/python/3.4.2/Python-3.4.2.tgz.asc
gpg --recv-keys 6A45C816 36580288 7D9DC8D2 18ADD4FF A4135B38 A74B06BF EA5BBD71 ED9D77D5 E6DF025C 6F5E1540 F73C700D
# TODO: Fail on bad condition
gpg --verify Python-3.4.2.tgz.asc
tar -xzf Python-3.4.2.tgz ~/Python-3.4.2
cd ~/Python-3.4.2
yes | sudo ./configure
yes | sudo make && sudo make altinstall
export PATH="$PATH:/usr/local/bin/python3.4"
wget https://bootstrap.pypa.io/ez_setup.py
sudo /usr/local/bin/python3.4 ez_setup.py
/usr/local/bin/easy_install pip
yes | sudo /usr/local/bin/pip install virtualenv
cd ~/
/usr/local/bin/virtualenv ografy_env
source ~/ografy_env/bin/activate

# Prep ografy project
cd ~/sites/ografy.io/www
yes | ~/ografy_env/bin/pip  install -r requirements/all.txt
yes | python manage.py migrate
yes | python manage.py validate
yes yes | sudo python manage.py collectstatic
echo export PYTHONPATH=~/ografy_env/bin/ >> ~/.bash_profile

# Prep SSL
openssl x509 -req -days 365 -in server.csr -signkey server.key -out server.crt
sudo cp /etc/nginx/sites-available/default /etc/nginx/sites-available/ografy.io

# Passenger dependances
yes | sudo yum install ruby rubygem-rake
yes | sudo yum install zlib-devel
yes | sudo yum install ruby-devel
yes | sudo /usr/bin/gem install rack
yes | sudo /usr/bin/gem install daemon_controller

# install passenger
sudo mkdir /opt/passenger
wget http://s3.amazonaws.com/phusion-passenger/releases/passenger-4.0.53.tar.gz
tar -xzvf passenger-4.0.53.tar.gz ~/
cd ~/passenger-4.0.53
yes | sudo ./bin/passenger-install-nginx-module --languages python
export PATH="$PATH:/opt/nginx/sbin"
sudo cp -r /sites/ografy.io/www/ografy/deploy/scripts/files/nginx /etc/init.d/
sudo chmod +x /etc/init.d/nginx
sudo cp -r /sites/ografy.io/www/ografy/deploy/scripts/files/nginx.conf /opt/nginx/conf/
sudo mkdir /opt/nginx/html/public
sudo cp -r /sites/ografy.io/www/ografy/passenger_wsgi.py /opt/nginx/html/public/
sudo systemctl daemon-reload
sudo /etc/init.d/nginx start
