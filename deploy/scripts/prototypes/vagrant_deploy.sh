#!/bin/bash
if [ ! $1 ]
then
 echo "No Vagrantfile specified."
 exit 1
fi

read -er -p "Username: " username
read -ers -p "Password: " password
echo
