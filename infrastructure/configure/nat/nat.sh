#!/bin/bash


WD=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )


umask 022
sudo cp -rv ${WD}/etc ${WD}/usr /
