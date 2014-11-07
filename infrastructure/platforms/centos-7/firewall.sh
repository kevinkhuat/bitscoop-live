#!/bin/bash


# Create installed checkpoints folder.
[ ! -d /installed ] && sudo mkdir /installed


# Flush iptables
sudo iptables -F
# Block all null packets
sudo iptables -A INPUT -p tcp --tcp-flags ALL NONE -j DROP
# Block all synflood packets
sudo iptables -A INPUT -p tcp ! --syn -m state --state NEW -j DROP
# Block all XMAS packets
sudo iptables -A INPUT -p tcp --tcp-flags ALL ALL -j DROP
# Open localhost interface
sudo iptables -A INPUT -i lo -j ACCEPT
# Accept web traffic
sudo iptables -A INPUT -p tcp -m tcp --dport 80 -j ACCEPT
sudo iptables -A INPUT -p tcp -m tcp --dport 443 -j ACCEPT
# Allow ssh traffic
sudo iptables -A INPUT -p tcp -m tcp --dport 22 -j ACCEPT
# Allow outgoing connections
sudo iptables -I INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT
# Allow outgoing connections
sudo iptables -P OUTPUT ACCEPT
# Block all other incoming connections
sudo iptables -P INPUT DROP

# Save firewall rules
sudo iptables-save | sudo tee /etc/sysconfig/iptables


touch /installed/firewall
