#!/bin/bash


FLAG=/installed/Python-3.4.2


install() {
    # Install dependencies.
    sudo yum install -y bzip2-devel gcc openssl-devel postgresql-devel python-devel sqlite-devel

    # Download source tarball if it doesn't already exist.
    [ ! -f ${HOME}/Python-3.4.2.tgz ] && wget -P ${HOME} https://www.python.org/ftp/python/3.4.2/Python-3.4.2.tgz

    # Verify tarball checksum.
    SHA512=863a2a2912ed872dbfd39888391210574c4cd5cf917af62ae2698c9ec74ad3dd6866ad8f1d43d6b1ca842eff40761021429aca41510bd1d004114a9b06996022

    if [ ! -n "`openssl dgst -sha512 ${HOME}/Python-3.4.2.tgz | grep ${SHA512}`" ]
    then
        echo "Invalid Python SHA512 checksum. Aborting..."
        exit 1
    fi

    # Extract source tarballs.
    [ ! -d ${HOME}/Python-3.4.2 ] && tar -xzf ${HOME}/Python-3.4.2.tgz -C ${HOME}

    # Perform installation.
    cd ${HOME}/Python-3.4.2
    # Configure install with the `with-ensurepip` flag set to install pip with Python (works with Python 3.4+)
    ./configure --with-ensurepip=install
    make
    sudo make altinstall


    # Ensure pip package manager is up to date
    sudo /usr/local/bin/pip3.4 install pip --upgrade
    # Install virtualenv to manage virtual Python environments
    sudo /usr/local/bin/pip3.4 install virtualenv


    # Create install checkpoint
    sudo mkdir -p `dirname ${FLAG}`
    sudo touch ${FLAG}
}


case ${1} in
    install)
        # Check to see if Python-3.4.2 is already installed.
        if [ -f ${FLAG} ]
        then
            echo "Python-3.4.2 already installed."
            exit 0
        fi

        install
        ;;
    uninstall)
        sudo rm -vf ${FLAG}
        echo "Python-3.4.2 uninstalled."
        ;;
    *)
        echo "Usage: ${0} {install|uninstall}"
        exit 1
        ;;
esac
