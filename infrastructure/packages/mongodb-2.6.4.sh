#!/bin/sh
# Create a yum repo file for Mongo so that we can install via yum package
# Need to create a temp file and copy it to the repos directory since the repo
# file cannot be modified directly
echo "Creating Mongo repo file"
TMP=`mktemp`
echo "[mongodb]
name=MongoDB Repository
baseurl=http://downloads-distro.mongodb.org/repo/redhat/os/x86_64/
gpgcheck=0
enabled=1" > ${TMP}
sudo cp ${TMP} /etc/yum.repos.d/mongodb.repo
sudo chmod 644 /etc/yum.repos.d/mongodb.repo
rm ${TMP}

#Install MongoDB from package
sudo yum install -y mongodb-org

#Start MongoDB
sudo service mongod start