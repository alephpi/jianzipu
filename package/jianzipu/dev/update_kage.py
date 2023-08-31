import csv
import operator
import yaml
from functools import reduce

with open('./dump_newest_only.txt', 'r', encoding='utf-8') as f:
  lines = f.readlines()
  lines = csv.reader(lines, delimiter='|')

all = {}
for i, line in enumerate(lines):
    if i <= 1 or len(line) < 3:
        continue
    line = [i.strip() for i in line]
    name, _, data = line
    # print(name, data)
    all[name] = data

with open('../jianzipu/kage.yaml', 'r', encoding='utf-8') as f:
   jianzi = yaml.safe_load(f)

jianzi = reduce(operator.ior, [*jianzi.values()], {})

# print(jianzi)
print(len(all))
def find_all_deps(name, dep_dict):
    dep_names = []
    if name in dep_dict:
        data = dep_dict[name]
        components = data.split('$')
        for component in components:
          if component[:2] == '99':
              dep_name = component.split(':')[7]
              dep_names.append(dep_name)
              dep_names.extend(find_all_deps(dep_name, dep_dict))
    return dep_names

# 给定的名称集合

closure = []
closure.extend(jianzi.values())
for name in jianzi.values():
    deps = find_all_deps(name, all)
    closure.extend(deps)

closure = set(closure)

sub = {k: v for k, v in all.items() if k in closure}

with open('../jianzipu/closure.yaml', 'w', encoding='utf-8') as f:
    yaml.safe_dump(sub, f, allow_unicode=True)