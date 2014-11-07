#!/bin/bash


# Create installed checkpoints folder.
[ ! -d /installed ] && sudo mkdir /installed

# Turn on time server
sudo chkconfig ntpd on
# Sync time
sudo ntpdate pool.ntp.org

touch /installed/time
