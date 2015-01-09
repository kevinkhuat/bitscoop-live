#!/bin/bash


SOURCE_DIR=`dirname ${BASH_SOURCE}`
source ${SOURCE_DIR}/../../common/parseargs.sh
source ${SOURCE_DIR}/../../common/baseline.sh


sudo -u ${CUSR} ${CUSR_HOME}/infrastructure/scripts/install/mongodb-2.7.8.sh


# Create log directory structure.
sudo mkdir -p /var/log/mongo


###################
# INSTALL SCRIPTS #
###################

# Start daemons.
sudo systemctl daemon-reload
sudo service mongod start
