#!/bin/bash
# @authors Kyle Baran, Liam Broza


# Establish variables
case "$1" in
    aws)
        echo Using aws settings.
        ;;
    virtual)
        echo Using virtual settings.
        ;;
    *)
        echo $"Usage: $0 {aws|virtual}"
        exit 2
        ;;
esac
