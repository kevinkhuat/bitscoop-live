#!/bin/bash


WD=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
source ${WD}/../baseline.sh


umask 022
sudo cp -rv ${WD}/etc ${WD}/usr /
