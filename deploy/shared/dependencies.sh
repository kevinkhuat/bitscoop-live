#!/bin/bash
# @authors Kyle Baran, Liam Broza


# Establish variables
case "$1" in
    aws)
        echo Using aws settings.

        # Create checkpoints folder.
        [ ! -d checkpoints ] && mkdir checkpoints

        sh os.sh aws
        sh python.sh aws
        sh passenger_nginx.sh aws
        sh web.sh aws

        ;;
    virtual)
        echo Using virtual settings.

        # Create checkpoints folder.
        [ ! -d checkpoints ] && mkdir checkpoints

        sh os.sh virtual
        sh python.sh virtual
        sh passenger_nginx.sh virtual
        sh firewall.sh virtual
        sh time.sh virtual
        sh web.sh virtual

        ;;
    *)
        echo $"Usage: $0 {production|virtual}"
        exit 2
        ;;
esac
