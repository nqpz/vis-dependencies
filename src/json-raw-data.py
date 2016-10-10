#!/usr/bin/env python3

import sys
import os
import json

data_dir = sys.argv[1]
out_file = sys.argv[2]

def read_file(fn):
    with open(fn) as f:
        return f.read().strip()

packages = []
for pdir in os.listdir(data_dir):
    name = read_file(os.path.join(data_dir, pdir, 'name'))
    version = read_file(os.path.join(data_dir, pdir, 'version'))
    modules = read_file(os.path.join(data_dir, pdir, 'modules')).split()
    dependencies = read_file(os.path.join(data_dir, pdir, 'dependencies')).split()
    imports = read_file(os.path.join(data_dir, pdir, 'imports')).split('\n')
    package = {
        'name': name,
        'version': version,
        'modules': modules,
        'dependencies': dependencies,
        'imports': imports
    }
    packages.append(package)

with open(out_file, 'w') as f:
    json.dump(packages, f, sort_keys=True, indent=2, ensure_ascii=False)
