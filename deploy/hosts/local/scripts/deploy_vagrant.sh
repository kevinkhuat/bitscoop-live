#!/bin/bash

cd $HOME/DEV/Repos
tar -czf ografy.tar.gz ografy --exclude-vcs --exclude-backups --exclude='.idea'
rm -rf $HOME/DEV/Packages/*
mv ografy.tar.gz $HOME/DEV/Packages

cp $HOME/DEV/Repos/ografy/deploy/scripts/dependencies.sh $HOME/DEV/Packages
cp $HOME/DEV/Repos/ografy/deploy/scripts/site.sh $HOME/DEV/Packages

chmod +x $HOME/DEV/Packages/*

cd $HOME/DEV/Repos/ografy/deploy/vagrant/local
vagrant up

vagrant ssh
cd /home/vagrant
sh site.sh virtual
