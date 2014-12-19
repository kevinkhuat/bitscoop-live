#!/bin/bash


usage() {
cat << EOF
usage: ${0} options

OPTIONS:
    -t    Host type. Can be \`production\` or \`virtual\`.
    -p    Platform. Can be \`ami\` or \`centos\`.

   [-f]  Force reinstallation of packages.
   [-r]  Full source rebuild of packages. Sets -f force flag to TRUE.
   [-s]  Django settings module to use. Overrides default associated with server type.
EOF
}


while getopts ":hfp:rs:t:" OPTION; do
    case ${OPTION} in
        h)
            usage
            exit 0
            ;;
        f)
            FORCE=1
            ;;
        p)
            PLATFORM=${OPTARG}
            ;;
        r)
            FORCE=1
            REBUILD=1
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
