#!/bin/sh

sudo yum install -y http://yum.postgresql.org/9.3/redhat/rhel-6-x86_64/pgdg-redhat93-9.3-1.noarch.rpm
sudo yum install -y postgresql93-server postgresql93-contrib
sudo /usr/pgsql-9.3/bin/postgresql93-setup initdb
sudo chkconfig postgresql-9.3 on
sudo service postgresql-9.3 start
sudo -u postgres createuser -d -r -s --replication ografy_db_user
sudo -u postgres createdb -O ografy_db_user ografy_db