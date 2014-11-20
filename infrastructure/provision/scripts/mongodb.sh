#!/bin/bash
# @authors Kyle Baran, Liam Broza


# Establish variables
case "$1" in
    aws)
        echo Using aws settings.

        cd /home/ec2-user

		CUSR=aws

         # Create checkpoints folder.
        [ ! -d checkpoints ] && mkdir checkpoints

        sh os.sh aws
        sh postgresql.sh aws

        ;;
    virtual)
        echo Using virtual settings.

        cd /home/vagrant

		CUSR=vagrant

        # Create checkpoints folder.
        [ ! -d checkpoints ] && mkdir checkpoints

        #sh os.sh virtual
        #sh postgresql.sh virtual

        ;;
    *)
        echo $"Usage: $0 {aws|virtual}"
        exit 2
        ;;
esac

case "$2" in
    force)
        echo Forcing all packages to reinstall

        [ -d /installed ] && sudo rm -rf /installed
        [ -d /packages ] && sudo rm -rf /packages

        /bin/su - $CUSR -c "sudo rm -rf /home/$CUSR/infrastructure"
        ;;

    *)
        ;;
esac

/bin/su - $CUSR -c "sudo tar -xf /home/$CUSR/infrastructure.tar.gz"

/bin/su - $CUSR -c "sh /home/$CUSR/infrastructure/packages/yum-update.sh"

/bin/su - $CUSR -c "sh /home/$CUSR/infrastructure/packages/mongodb.sh"
