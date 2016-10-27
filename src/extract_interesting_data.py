#!/usr/bin/env python3

import sys
import os
import json

in_file = sys.argv[1]
in_github_file = sys.argv[2]
out_file = sys.argv[3]

with open(in_file) as f:
    packages = json.load(f)

with open(in_github_file) as f:
    packages_github = json.load(f)
    
dic = {}
for p in packages:
    dic[p['name']] = p

dic_github = {}
for p in packages_github:
    dic_github[p['name']] = p

# github_max = {
#     'stargazers_count': 0,
#     'subscribers_count': 0,
#     'forks': 0,
#     'watchers': 0,
#     'open_issues_count': 0
# }

# for p in packages_github:
#     dic_github[p['name']] = p

#     pg = p['Repo']
#     if pg:
#         for k in github_max.keys():
#             github_max[k] += pg[k]
    
def number_of_reverse_dependencies(n):
    s = 0
    for p in packages:
        if n in p['dependencies_core'].keys() \
           or n in p['dependencies_testbench'].keys():
            s += 1
    return s

packages1 = []
    
for p in packages:
    dependencies = (list(p['dependencies_core'].items())
                    + list(p['dependencies_testbench'].items()))
    dependencies1 = {}
    for d_p, d_ms in dependencies:
        dependencies1[d_p] = set()
    for d_p, d_ms in dependencies:
        dependencies1[d_p] = dependencies1[d_p].union(set(d_ms))
    dependencies2 = []
    maximums = {
        'number_of_uses': 0,
        'github' : {
            'stargazers_count': 0,
            'subscribers_count': 0,
            'forks': 0,
            'watchers': 0,
            'open_issues_count': 0
        }
    }
            
    for d_p, d_ms in dependencies1.items():
        try:
            d_pa = dic[d_p]
        except KeyError:
            continue
        
        pg = dic_github[d_p]['Repo']
        if pg:
            github_data = {
                'stargazers_count': pg['stargazers_count'],
                'subscribers_count': pg['subscribers_count'],
                'forks': pg['forks'],
                'watchers': pg['watchers'],
                'open_issues_count': pg['open_issues_count']
            }
        else:
            github_data = None
            
        d = {
            'name': d_p,
            'number_of_modules': len(d_ms),
            'total_number_of_modules': len(d_pa['modules']),
            'number_of_uses': number_of_reverse_dependencies(d_p),
            'github': github_data
        }
        dependencies2.append(d)

        maximums['number_of_uses'] = max(maximums['number_of_uses'],
                                         d['number_of_uses'])
        if github_data:
            for k, v in github_data.items():
                maximums['github'][k] = max(maximums['github'][k], v)
        
    p1 = {
        'name': p['name'],
        'dependencies': dependencies2,
        'maximums': maximums
    }
    packages1.append(p1)

packages1.sort(key=lambda p: p['name'])

for p in packages1:
    for d in p['dependencies']:
        index = None
        for p1, i in zip(packages1, range(len(packages1))):
            if p1['name'] == d['name']:
                index = i
                break
        if index is None:
            print(d['name'])
        d['index'] = index

    
# d = {
#     'github_maximum': github_max,
#     'packages': packages1
# }
    
with open(out_file, 'w') as f:
    json.dump(packages1, f, sort_keys=True, indent=2, ensure_ascii=False)
