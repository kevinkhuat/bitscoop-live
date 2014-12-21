#!/bin/sh

cd /

sudo yum install -y postgresql-devel

#Install the PostgreSQL 9.3 YUM repository and then install the PostgreSQL packages
sudo yum install -y http://yum.postgresql.org/9.3/redhat/rhel-6-x86_64/pgdg-redhat93-9.3-1.noarch.rpm
sudo yum install -y postgresql93-server postgresql93-contrib

#Set PostgreSQL to automatically start and be initialized
sudo /usr/pgsql-9.3/bin/postgresql93-setup initdb
sudo chkconfig postgresql-9.3 on

#Start PostgreSQL service
sudo service postgresql-9.3 start

#Create the ografy DB user and then create the ografy DB with them as the owner
sudo -u postgres createuser -d -r -s --replication ografy_db_user
sudo -u postgres createdb -O ografy_db_user ografy_db
