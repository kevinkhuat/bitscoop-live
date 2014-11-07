#!/bin/bash


# Create installed checkpoints folder.
[ ! -d /installed ] && sudo mkdir /installed && sudo chmod -R 777 /installed

[ -f /installed/time ] && [ "$1" != "force" ] && echo time already installed. && exit 0

# Turn on time server
sudo chkconfig ntpd on
# Sync time
sudo ntpdate pool.ntp.org

touch /installed/time
