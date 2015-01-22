#!/bin/bash


WD=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
source ${WD}/../baseline.sh


sudo yum install -y --disablerepo=* --enablerepo=ografy redis stunnel


umask 022
sudo cp -rv ${WD}/etc /


sudo chkconfig stunnel on
sudo service stunnel start

sudo chkconfig redis on
sudo service redis start
