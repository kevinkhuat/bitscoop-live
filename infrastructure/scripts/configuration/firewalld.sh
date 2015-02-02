#!/bin/bash


bold=`tput bold`
normal=`tput sgr0`


# TODO: Make this work for more than one interface.
INTERFACE=`sudo firewall-cmd --list-all-zones | grep -Po "(?<=interfaces: ).*"`
ZONES=`sudo firewall-cmd --get-zones`


if [ -z "`echo ${ZONES} | grep development`" ]
then
    echo -n "Creating zone ${bold}development${normal}..."
    sudo firewall-cmd --new-zone development --permanent
    REBOOT=1
fi

if [ -z "`echo ${ZONES} | grep database`" ]
then
    echo -n "Creating zone ${bold}database${normal}..."
    sudo firewall-cmd --new-zone database --permanent
    REBOOT=1
fi

if [ -z "`echo ${ZONES} | grep webserver`" ]
then
    echo -n "Creating zone ${bold}webserver${normal}..."
    sudo firewall-cmd --new-zone webserver --permanent
    REBOOT=1
fi

if [ ${REBOOT+x} ]
then
    echo -n "Propagating zone changes... "
    sudo firewall-cmd --reload
    echo
fi


echo -n "Adding ${bold}http${normal} interface to ${bold}development${normal} zone... "
sudo firewall-cmd --zone development --add-service http --permanent
echo -n "Adding ${bold}https${normal} interface to ${bold}development${normal} zone... "
sudo firewall-cmd --zone development --add-service https --permanent
echo -n "Adding ${bold}ssh${normal} interface to ${bold}development${normal} zone... "
sudo firewall-cmd --zone development --add-service ssh --permanent
echo -n "Adding port ${bold}27017/tcp${normal} to ${bold}development${normal} zone... "
sudo firewall-cmd --zone development --add-port 27017/tcp --permanent
echo -n "Adding port ${bold}5432/tcp${normal} to ${bold}development${normal} zone... "
sudo firewall-cmd --zone development --add-port 5432/tcp --permanent
echo


echo -n "Adding ${bold}http${normal} interface to ${bold}webserver${normal} zone... "
sudo firewall-cmd --zone webserver --add-service http --permanent
echo -n "Adding ${bold}https${normal} interface to ${bold}webserver${normal} zone... "
sudo firewall-cmd --zone webserver --add-service https --permanent
echo


echo -n "Adding port ${bold}27017/tcp${normal} to ${bold}database${normal} zone... "
sudo firewall-cmd --zone database --add-port 27017/tcp --permanent
echo -n "Adding port ${bold}5432/tcp${normal} to ${bold}database${normal} zone... "
sudo firewall-cmd --zone database --add-port 5432/tcp --permanent
echo


echo -n "Assigning interface ${bold}${INTERFACE}${normal} to zone ${bold}development${normal}... "
sudo firewall-cmd --zone development --change-interface ${INTERFACE}
echo


echo -n "Setting zone ${bold}development${normal} to default..."
sudo firewall-cmd --set-default-zone=development
echo


echo -n "Propagating rule changes... "
sudo firewall-cmd --reload


sudo service network restart
