#!/bin/bash


WD=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
source ${WD}/../baseline.sh


sudo yum install -y createrepo gcc gcc-c++ git openssl-devel rpm rpm-build


wget http://superb-dca2.dl.sourceforge.net/project/scons/scons/2.3.4/scons-2.3.4.tar.gz
umask 002
tar -xzf scons-2.3.4.tar.gz
cd scons-2.3.4
sudo python setup.py install


wget https://storage.googleapis.com/golang/go1.3.3.linux-amd64.tar.gz
sudo tar -xzf go1.3.3.linux-amd64.tar.gz -C /usr/local
TMP=`mktemp`
cat << EOF > ${TMP}
export PATH=\${PATH}:/usr/local/go/bin
EOF
sudo mv ${TMP} /etc/profile.d/go.sh
sudo chown root:root /etc/profile.d/go.sh
sudo chmod 644 /etc/profile.d/go.sh
