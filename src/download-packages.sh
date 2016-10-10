#!/bin/sh

set -e # Exit on first error.

version="$1"
outdir="$2"

if ! [ "$version" ]; then
    echo 'error: specify a version, e.g. lts-7.3'
    exit 1
fi

if ! [ "$outdir" ]; then
    echo 'error: specify an output directory'
    exit 1
fi

base="$(readlink -f "$(dirname "$0")")"

mkdir -p "$outdir"
cd "$outdir"

# Unpacking seems to fail for a few packages, notably ghc-* and rts-*.
# Works otherwise.
for package in $("$base/get-package-names.sh" "$version"); do
    stack unpack $package
done
