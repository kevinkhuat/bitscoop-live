#!/bin/bash


SOURCE_DIR=`dirname ${BASH_SOURCE}`
source ${SOURCE_DIR}/../../common/parseargs.sh
source ${SOURCE_DIR}/../../common/baseline.sh


# Create log directory structure.
sudo mkdir -p /var/log/mongo

mkdir tmp
sudo mount /dev/sdf tmp

TMP=`mktemp`
cat << EOF > ${TMP}
[mongodb]
name=Local MongoDB Repository
baseurl=file://`echo ${HOME}`/tmp/repo
gpgcheck=0
enabled=1
EOF
sudo cp ${TMP} /etc/yum.repos.d/local-mongodb.repo
sudo chmod 644 /etc/yum.repos.d/local-mongodb.repo
rm ${TMP}

sudo yum install -y mongodb-org

sudo umount tmp
rm -r tmp
sudo rm /etc/yum.repos.d/local-mongodb.repo


###################
# INSTALL SCRIPTS #
###################

# Copy daemon scripts
sudo cp ${CUSR_HOME}/infrastructure/scripts/init.d/mongod /etc/init.d
sudo chmod +x /etc/init.d/mongod

# Start daemons.
sudo systemctl daemon-reload
sudo service mongod start
