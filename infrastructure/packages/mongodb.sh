#!/bin/sh
curl -O http://downloads.mongodb.org/linux/mongodb-linux-x86_64-2.6.4.tgz
tar -zxvf mongodb-linux-x86_64-2.6.4.tgz
mkdir -p mongodb
cp -R -n mongodb-linux-x86_64-2.6.4/ mongodb
sudo mkdir /data
sudo mkdir /data/db
mongod