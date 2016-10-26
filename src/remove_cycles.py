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
    
def check(p_name):
    return _check([], p_name)
    
def _check(visited, p_name):
    if p_name in visited:
        return True
    visited1 = visited + [p_name]
    p = dic[p_name]
    dkeys = p['dependencies_core'].keys()
    for d in dkeys:
        try:
            dp = dic[d]
        except KeyError:
            continue
        if _check(visited1, dp['name']):
            return True
    return False

pkeep = []
for p in packages:
    # if check(p['name']):
    #     print(p['name'])
    if not check(p['name']):
        pkeep.append(p)

with open(out_file, 'w') as f:
    json.dump(pkeep, f, sort_keys=True, indent=2, ensure_ascii=False)
