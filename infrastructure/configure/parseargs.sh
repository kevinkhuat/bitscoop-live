#!/bin/bash


usage() {
cat << EOF
usage: ${0} options

OPTIONS:
    -t    Host type. Can be \`production\` or \`virtual\`.

   [-s]  Django settings module to use. Overrides default associated with server type.
EOF
}


# Set default values for variables should another script be calling this one.
CUSR=ec2-user
CUSR_HOME=`sudo su - ${CUSR} -c "echo ${HOME}"`


# Parse options.
while getopts ":hs:t:" OPTION; do
    case ${OPTION} in
        h)
            usage
            exit 0
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


# Check option validity.
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
