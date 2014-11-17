#!/bin/bash

# Turn on time server
sudo chkconfig ntpd on
# Sync time
sudo ntpdate pool.ntp.org
