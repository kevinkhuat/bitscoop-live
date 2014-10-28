#!/bin/sh
# This file bootstraps deployment from vagrantfile for dev test and production
# @authors Kyle Baran, Liam Broza
yes | sudo sh 1_deploy_bootstrap_update_os.sh
yes | sudo sh 2_deploy_bootstrap_nginx.sh
yes | sudo sh 3_deploy_bootstrap_passanger.sh
yes | sudo sh 4_deploy_bootstrap_python.sh
yes | sudo sh 5_deploy_bootstrap_ografy.sh $1 $2
yes | sudo sh 6_deploy_bootstrap_ssl.sh
yes | sudo sh 7_deploy_bootstrap_config.sh
