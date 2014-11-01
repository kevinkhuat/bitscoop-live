#!/bin/bash

# Start time sync daemon
# TODO: Find out why this doesn't work.
#sudo /etc/init.d/ntpd start

sudo systemctl daemon-reload

# Only fresh start the nginx process if it doesn't already exist.
[ ! -n "`pgrep -fl /opt/nginx/sbin/nginx`" ] && sudo service nginx start &
sudo /opt/nginx/sbin/nginx -s reload
