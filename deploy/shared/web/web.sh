#!/bin/bash
# @authors Kyle Baran, Liam Broza


# Establish variables
case "$1" in
    aws)
        echo Using aws settings.

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

        cd /home/vagrant

        # Create checkpoints folder.
        [ ! -d checkpoints ] && mkdir checkpoints

        sh os.sh virtual
        sh python.sh virtual
        sh passenger.sh virtual
        sh firewall.sh virtual
        sh time.sh virtual
        sh ografy.sh virtual

        ;;
    *)
        echo $"Usage: $0 {aws|virtual}"
        exit 2
        ;;
esac
