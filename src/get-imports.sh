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
            grep -Eo '^import\s+(qualified)?\s*([A-Z][A-Za-z]*\.?)+' "$filename" \
                | sed 's/ qualified//' \
                | cut -d' ' -f2
        done
    } \
    | sort \
    | uniq \
    | grep .

exit 0
