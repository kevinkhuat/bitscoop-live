#!/bin/bash
# @authors Kyle Baran, Liam Broza


# Establish variables
case "$1" in
    aws)
        echo Using aws settings for web config.

        CUSR=ec2-user
        ;;

    virtual)
        echo Using virtual settings for web config.

        # TODO: Change to ec2-user to match production more closely
        CUSR=vagrant
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

case "$1" in
    virtual)
        # sh ~/infrastructure/platforms/centos-7/ografy-user.sh
        /bin/su - $CUSR -c "sh /home/$CUSR/infrastructure/platforms/centos-7/firewall.sh"
        /bin/su - $CUSR -c "sh /home/$CUSR/infrastructure/platforms/centos-7/time.sh"
        ;;
esac

/bin/su - $CUSR -c "sh /home/$CUSR/infrastructure/packages/python-3.4.2.sh"
/bin/su - $CUSR -c "sh /home/$CUSR/infrastructure/packages/passenger-4.0.53.sh"
/bin/su - $CUSR -c "sh /home/$CUSR/infrastructure/packages/ografy-0.2.0.sh virtual"

sudo /etc/init.d/./nginx start
