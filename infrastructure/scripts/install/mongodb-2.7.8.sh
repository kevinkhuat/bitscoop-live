#!/bin/sh


FLAG=/installed/mongodb-2.7.8


######################
# CREATE MOUNT POINT #
######################

MNT=`mktemp -d`
sudo mount /dev/sdf ${MNT}


if [ "$?" -ne "0" ]
then
    rm -r ${MNT}
    exit $?
fi


#####################
# CREATE LOCAL REPO #
#####################

REPO=`mktemp`
cat << EOF > ${REPO}
[mongodb]
name=Ografy Repository
baseurl=file://${MNT}/repo
gpgcheck=0
enabled=1
EOF
sudo cp ${REPO} /etc/yum.repos.d/ografy.repo
sudo chmod 644 /etc/yum.repos.d/ografy.repo
rm ${REPO}


###########
# INSTALL #
###########

sudo yum install -y mongodb-org

# Create install checkpoint
sudo mkdir -p `dirname ${FLAG}`
sudo touch ${FLAG}


############
# CLEAN UP #
############

sudo umount ${MNT}
rm -r ${MNT}
sudo rm /etc/yum.repos.d/ografy.repo
