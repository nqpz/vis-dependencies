#!/bin/sh
#
# Get the names of all Stackage packages for a certain snapshot.

version="$1"

if ! [ "$version" ]; then
    echo 'error: specify a version, e.g. lts-7.3'
    exit 1
fi

curl --silent https://www.stackage.org/lts-7.3 \
    | grep -Po '(?<=>)[^<]+(?=</a>)' \
    | tail -n +5 \
    | head -n -1
