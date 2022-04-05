# -*- coding: utf-8 -*-
# @Time    : 2021-11-08 16:46
# @Author  : sanclark
# @Mail    : sanclark@qq.com

import pickle
from HostUtil import getHost
fn = 'blacklist20211108.tpl'
wdic = pickle.load(open(fn, 'rb')) #type: dict
i = 0
kl = ['t', 'l']
tList = []
hDic = set()
for k, v in wdic.items():
    host = k.replace("blacklist:", "")
    d, name, c = getHost(host)
    hDic.add(d)
    line = "{}\t".format(host)
    for ki in kl:
        line += "{}\t".format(v[ki])
    tList.append(line)

print(len(hDic))


with open(fn.replace('tpl', 'txt'), 'w', encoding='utf-8') as f:
    f.write('\n'.join(tList))