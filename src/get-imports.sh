#!/bin/sh
#
# Extract imports from all Haskell files in a directory.

dir="$1"

if ! [ "$dir" ]; then
    echo 'error: specify a directory'
    exit 1
fi

find "$dir" -name '*.hs' \
    | grep -v Setup.hs \
    | \
    {
        while read filename; do
            grep -E '^import +qualified? *[A-Z]' "$filename" \
                | sed 's/ qualified//' \
                | cut -d' ' -f2
        done
    } \
    | sort \
    | uniq \
    | grep .
