#!/bin/sh

set -e # Exit on first error.

pacdir="$1"
outdir="$2"

if ! [ "$pacdir" ]; then
    echo 'error: specify a package directory'
    exit 1
fi

if ! [ "$outdir" ]; then
    echo 'error: specify an output directory'
    exit 1
fi

base="$(readlink -f "$(dirname "$0")")"

outdir="$(readlink -f "$outdir")"

mkdir -p "$outdir"

stack ghc -- -O3 $base/get-description.hs

cd "$pacdir"
for dir in *; do
    name="$(echo "$dir" | sed -r 's/-[^-]+$//')"
    version="$(echo "$dir" | grep -Eo '[^-]+$')"
    cabal_file="$(echo "$dir/"*.cabal)"
    resdir="$outdir/$name"
    echo $name
    mkdir "$resdir"
    echo $name > "$resdir/name"
    echo $version > "$resdir/version"
    "$base/get-imports.sh" "$dir" > "$resdir/imports"
    "$base/get-description" "$cabal_file" | {
        read modules
        read dependencies
        echo $modules > "$resdir/modules"
        echo $dependencies > "$resdir/dependencies"
        while read repo_type && read repo_url; do
            echo "$repo_type" > "$resdir/repo_type"
            echo "$repo_url" > "$resdir/repo_url"
        done
    }
done
