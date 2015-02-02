#!/bin/bash


WD=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )


sudo yum install -y --disablerepo=* --enablerepo=ografy mongodb-org


umask 022
sudo cp -rv ${WD}/etc /


sudo chkconfig mongod on
sudo service mongod start
