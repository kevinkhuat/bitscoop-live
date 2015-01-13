#!/bin/bash
# Configure the instance to run as a Port Address Translator (PAT) to provide
# Internet connectivity to private instances.


function log { logger -t "vpc" -- $1; }


function die {
    [ -n "$1" ] && log "$1"
    log "Configuration of PAT failed!"
    exit 1
}


# Sanitize PATH
PATH="/usr/sbin:/sbin:/usr/bin:/bin"


log "Determining the MAC address on eth0..."
ETH0_MAC=$(cat /sys/class/net/eth0/address) ||
    die "Unable to determine MAC address on eth0."
log "Found MAC ${ETH0_MAC} for eth0."


VPC_CIDR_RANGE="10.0.0.0/16"
log "Enabling PAT..."
sysctl -q -w net.ipv4.ip_forward=1 net.ipv4.conf.eth0.send_redirects=0 &&
    (iptables -t nat -C POSTROUTING -o eth0 -s ${VPC_CIDR_RANGE} -j MASQUERADE 2> /dev/null ||
    iptables -t nat -A POSTROUTING -o eth0 -s ${VPC_CIDR_RANGE} -j MASQUERADE) ||
    die


sysctl net.ipv4.ip_forward net.ipv4.conf.eth0.send_redirects | log
iptables -n -t nat -L POSTROUTING | log


log "Configuration of PAT complete."
exit 0
