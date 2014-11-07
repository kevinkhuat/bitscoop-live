#!/bin/bash


# Create installed checkpoints folder.
[ ! -d /installed ] && sudo mkdir /installed && sudo chmod -R 777 /installed


[ -f /installed/time ] && echo time already configured. && exit 0

# Turn on time server
sudo chkconfig ntpd on
# Sync time
sudo ntpdate pool.ntp.org

sudo touch /installed/time
