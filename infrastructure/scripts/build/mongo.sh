#!/bin/bash


#############
# VARIABLES #
#############

WD=`pwd`
VERSION=mongodb-org-2.7.8
MONGODB=${HOME}/Development/Repositories/mongo
MONGOTOOLS=${HOME}/Development/Repositories/mongo-tools


###############
# MAIN SCRIPT #
###############

TMP=`mktemp -d`
RPM=${WD}/rpmbuild
SPECS=${RPM}/SPECS


# Create directory structure.
mkdir -vp ${WD}/rpmbuild/{BUILD,RPMS,SOURCES,SPECS,SRPMS}

# Link build specification.
ln -v ${MONGODB}/rpm/mongodb-org.spec ${RPM}/SPECS


# Create sources tarball (required for the build specification profile).
if [ ! -f ${RPM}/SOURCES/${VERSION}.tar.gz ]
then
    OUTPUT=${TMP}/build/${VERSION}
    BIN=${OUTPUT}/BINARIES/usr/bin
    DOCS=${OUTPUT}/debian
    CONF=${OUTPUT}/rpm

    # Create directory structure.
    mkdir -vp ${BIN} ${DOCS} ${CONF}

    # Link compiled binaries.
    find ${MONGODB}/build/linux2/64/ssl/mongo -type f -perm /a+x -exec ln -v {} ${BIN} \;
    find ${MONGOTOOLS}/bin -type f -perm /a+x -exec ln -v {} ${BIN} \;

    # Link documentation files.
    ln -v ${MONGODB}/debian/*.1 ${DOCS}

    # Link configuration files.
    ln -v ${MONGODB}/rpm/init.d-mongod ${CONF}
    ln -v ${MONGODB}/rpm/mongod.conf ${CONF}
    ln -v ${MONGODB}/rpm/mongod.sysconfig ${CONF}

    # Create source tarball.
    CWD=`pwd`
    cd ${OUTPUT}/..
    tar -cpzvf ${RPM}/SOURCES/${VERSION}.tar.gz ${VERSION}/
    cd ${CWD}
fi


# Create build macro.
MACROFILE=${TMP}/macros
cat << EOF > ${MACROFILE}
%_topdir ${RPM}
%_arch x86_64
EOF


# Run rpm build process.
rpmbuild -ba --target x86_64 --macros /usr/lib/rpm/macros:/usr/lib/rpm/x86_64-linux/macros:/etc/rpm/macros.*:/etc/rpm/macros:/etc/rpm/x86_64-linux/macros:~/.rpmmacros:${MACROFILE} ${SPECS}/mongodb-org.spec


# Clean up.
rm -rf ${TMP}
