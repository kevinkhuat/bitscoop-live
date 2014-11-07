#!/bin/bash
# @authors Kyle Baran, Liam Broza


# Establish variables
case "$1" in
    aws)
        echo Using aws settings for web config.

        # Set environment variable for django
        export DJANGO_SETTINGS_MODULE='ografy.settings.production'

        cd /home/ec2-user

        ;;
    virtual)
        echo Using virtual settings for web config.

        # Set environment variable for django
        export DJANGO_SETTINGS_MODULE='ografy.settings.virtual'

        # TODO: Change to ec2-user to match aws
        cd /home/vagrant

        ;;
    *)
        echo $"Usage: $0 {aws|virtual}"
        exit 2
        ;;
esac

tar -xf ~/infrastructure.tar.gz

# Create installed checkpoints folder.
[ ! -d /installed ] && sudo mkdir /installed

# Create packages folder.
[ ! -d /packages ] && sudo mkdir /packages

sh infrastructure/packages/yum-update.sh
sh infrastructure/packages/Python-3.4.2.sh
sh infrastructure/packages/passenger-3.0.53.sh
sh infrastructure/packages/ografy-0.2.0.sh virtual
