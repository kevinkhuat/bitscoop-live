#!/bin/bash


sudo cp -v ./rc.d/rc.local /etc/rc.d/
sudo chmod 755 /etc/rc.d/rc.local

sudo cp -v ./sbin/configure-pat.sh /usr/local/sbin/
sudo chmod 755 /usr/local/sbin/configure-pat.sh
