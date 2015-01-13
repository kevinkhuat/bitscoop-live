#!/bin/bash


usage() {
cat << EOF
usage: ${0} options

OPTIONS:
    -t    Host type. Can be \`production\` or \`virtual\`.
    -p    Platform. Can be \`ami\` or \`centos\`.

   [-s]  Django settings module to use. Overrides default associated with server type.
EOF
}


while getopts ":hp:s:t:" OPTION; do
    case ${OPTION} in
        h)
            usage
            exit 0
            ;;
        p)
            PLATFORM=${OPTARG}
            ;;
        s)
            SETTINGS=${OPTARG}
            ;;
        t)
            TYPE=${OPTARG}
            ;;
        ?)
            usage
            exit 1
            ;;
    esac
done


case ${TYPE} in
    production)
        ;;
    virtual)
        ;;
    *)
        echo "Invalid type: ${TYPE}"
        exit 1
        ;;
esac


CUSR_HOME=`sudo su - ${CUSR} -c "echo ${HOME}"`


case ${PLATFORM} in
    ami)
        ;;
    centos)
        ;;
    *)
        echo "Invalid platform: ${PLATFORM}"
        exit 1
        ;;
esac
