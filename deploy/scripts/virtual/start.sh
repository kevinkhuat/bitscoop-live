#!/bin/bash

# Start time sync daemon
# TODO: Find out why this doesn't work.
#sudo /etc/init.d/ntpd start

# FIXME: These two lines are necessary to handle a known bug of the nginx version installed with Passenger.
sudo systemctl daemon-reload
sudo /etc/init.d/nginx start

sudo /opt/nginx/sbin/nginx -s reload
