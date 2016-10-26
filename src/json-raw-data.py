#!/usr/bin/env python3

import sys
import os
import json

data_dir = sys.argv[1]
out_file = sys.argv[2]

def read_file(fn):
    try:
        with open(fn) as f:
            return f.read().strip()
    except FileNotFoundError:
        return

packages = []
for pdir in os.listdir(data_dir):
    name = read_file(os.path.join(data_dir, pdir, 'name'))
    version = read_file(os.path.join(data_dir, pdir, 'version'))
    modules = read_file(os.path.join(data_dir, pdir, 'modules')).split()
    dependencies_core = read_file(os.path.join(data_dir, pdir, 'dependencies_core')).split()
    if name in dependencies_core:
        dependencies_core.remove(name)
    dependencies_testbench = read_file(os.path.join(data_dir, pdir, 'dependencies_testbench')).split()
    if name in dependencies_testbench:
        dependencies_testbench.remove(name)
    imports = read_file(os.path.join(data_dir, pdir, 'imports')).split('\n')
    repo_type = read_file(os.path.join(data_dir, pdir, 'repo_type'))
    repo_url = read_file(os.path.join(data_dir, pdir, 'repo_url'))
    if repo_type and repo_url:
        repo = {
            'type': repo_type,
            'url': repo_url
        }
    else:
        repo = {}

    package = {
        'name': name,
        'version': version,
        'modules': modules,
        'dependencies_core': dependencies_core,
        'dependencies_testbench': dependencies_testbench,
        'imports': imports,
        'repo': repo
    }
    packages.append(package)

with open(out_file, 'w') as f:
    json.dump(packages, f, sort_keys=True, indent=2, ensure_ascii=False)
