# -*- coding:utf-8 -*-
import glob
import os.path

from settings import DUMP_DIR

from loguru import logger

# a = set(['a','b','c','d','e','f','g'])
# n = set(['1','2','c','d','e'])
#
# print(a.difference(n))
# print(n.difference(a))
# print(a.intersection(n))



files = glob.glob(os.path.join(DUMP_DIR, 'tac_*.text'))
file = sorted(files, reverse=True)[0]

new_tacs_dict = {}
old_tacs_dict = {}

with open(os.path.join(DUMP_DIR, file), encoding='utf-8') as f:
    for line in f.readlines():
        k, v = line.split('|', 1)
        new_tacs_dict[k] = line.strip()
    new_tacs = set(new_tacs_dict.keys())
    print('new集合: ', len(new_tacs))

with open('../backup/tac.2021.text', encoding='utf-8') as o:
    for line in o.readlines():
        k, v = line.split(',', 1)
        old_tacs_dict[k] = line.strip()
    old_tacs = set(old_tacs_dict.keys())
    print('old集合: ', len(old_tacs))

# new - old
diff_new_minus_old_tac = new_tacs.difference(old_tacs)

# old - new
diff_old_minus_new_tac = old_tacs.difference(new_tacs)

# new + old
union_tac = new_tacs.union(old_tacs)

logger.debug('old tac size: {}', len(old_tacs))
logger.debug('new tac size: {}', len(new_tacs))
logger.debug('new - old size: {}', len(diff_new_minus_old_tac))
logger.debug('old - new size: {}', len(diff_old_minus_new_tac))
logger.debug('union size: {}', len(union_tac))

with open(os.path.join(DUMP_DIR, 'new_diff.text'), mode='w', encoding='utf-8') as f:
    for tac in diff_new_minus_old_tac:
        f.write(new_tacs_dict[tac] + '\n')

with open(os.path.join(DUMP_DIR, 'old_diff.text'), mode='w', encoding='utf-8') as f:
    for tac in diff_old_minus_new_tac:
        f.write(old_tacs_dict[tac] + '\n')