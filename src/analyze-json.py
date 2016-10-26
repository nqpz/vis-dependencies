#!/usr/bin/env python3

import sys
import os
import json

json_file = sys.argv[1]
out_file = sys.argv[2]

with open(json_file) as f:
    packages = json.load(f)

dic = {}

for p in packages:
    dic[p['name']] = p

for p in packages:
    deps = p['dependencies_core']
    imps = p['imports']

    ms = {}
    for dep in deps:
        try:
            p1 = dic[dep]
        except KeyError:
            continue
        for m in p1['modules']:
            ms[m] = dep
    deps_new = {}
    for dep in deps:
        deps_new[dep] = []

    for imp in imps:
        if imp in p['modules']:
            continue
        try:
            imp_dep = ms[imp]
        except KeyError:
            print('warning: module {} was not found, imported from {} (probably an internal module or a source cabal file with flags)'.format(imp, p['name']), file=sys.stderr)
            continue
        deps_new[imp_dep].append(imp)

    p['dependencies_core'] = deps_new


    deps = p['dependencies_testbench']
    imps = p['imports']

    ms = {}
    for dep in deps:
        try:
            p1 = dic[dep]
        except KeyError:
            continue
        for m in p1['modules']:
            ms[m] = dep
    deps_new = {}
    for dep in deps:
        deps_new[dep] = []

    for imp in imps:
        if imp in p['modules']:
            continue
        try:
            imp_dep = ms[imp]
        except KeyError:
            print('warning: module {} was not found, imported from {} (probably an internal module or a source cabal file with flags)'.format(imp, p['name']), file=sys.stderr)
            continue
        deps_new[imp_dep].append(imp)

    p['dependencies_testbench'] = deps_new

with open(out_file, 'w') as f:
    json.dump(packages, f, sort_keys=True, indent=2, ensure_ascii=False)
