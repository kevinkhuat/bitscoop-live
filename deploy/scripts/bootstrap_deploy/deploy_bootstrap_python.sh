#!/bin/sh
# @authors Kyle Baran, Liam Broza
cd /
yes | sudo yum install python-devel
yes | sudo yum install libffi-devel
yes | sudo yum install bzip2-devel
sudo wget https://www.python.org/ftp/python/3.4.1/Python-3.4.1.tar.xz
sudo xz -d Python-3.4.1.tar.xz
sudo tar -xvf Python-3.4.1.tar
cd Python-3.4.1
sudo ./configure
sudo make && sudo make altinstall
export PATH="$PATH:/usr/local/bin/python3.4"
# curl https://raw.github.com/pypa/pip/master/contrib/get-pip.py | sudo python3.4 -
wget https://bootstrap.pypa.io/ez_setup.py -O - | sudo python3.4
sudo mkdir /ografy
sudo /usr/local/bin/pip3.4 install virtualenv
cd /ografy/
sudo /usr/local/bin/virtualenv /ografy/ografy_env
source /ografy/ografy_env/bin/activate
