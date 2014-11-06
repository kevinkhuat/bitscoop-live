#!/bin/bash
# @authors Kyle Baran, Liam Broza


# Establish variables
case "$1" in
    aws)
        echo Using aws settings.

        # Set environment variable for django
        export DJANGO_SETTINGS_MODULE='ografy.settings.production'

        cd /home/ec2-user

        # Create checkpoints folder.
        [ ! -d checkpoints ] && mkdir checkpoints

        sh os.sh aws
        sh python.sh aws
        sh passenger.sh aws
        sh ografy.sh aws

        ;;
    virtual)
        echo Using virtual settings.

        # Set environment variable for django
        export DJANGO_SETTINGS_MODULE='ografy.settings.virtual'

        cd /home/vagrant

        # Create checkpoints folder.
        [ ! -d ~/checkpoints ] && mkdir ~/checkpoints

        # Create packages folder.
        [ ! -d ~/packages ] && mkdir ~/packages

        sh scripts/os.sh virtual
        sh scripts/python.sh virtual
        sh scripts/passenger.sh virtual
        sh scripts/firewall.sh virtual
        sh scripts/time.sh virtual
        sh scripts/ografy.sh virtual

        ;;
    *)
        echo $"Usage: $0 {aws|virtual}"
        exit 2
        ;;
esac
