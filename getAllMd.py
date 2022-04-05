# -*- coding: utf-8 -*-
# @Time    : 2021-06-21 17:02
# @Author  : sanclark
# @Mail    : sanclark@qq.com

import redis
import time
r = redis.Redis(host='127.0.0.1', port=6379, decode_responses=True)
bg = 0
total = 0
mdList = []
while True:
    rt, dl = r.scan(bg, 'md:*', 10000)
    if len(dl) > 0:
        total += len(dl)
        # for d in dl:
        #     v = r.hgetall(d)
        #     print(v)
        for d in dl:
            mdList.append(d.replace("md:", ""))
    if rt == 0:
        break
    bg = rt

with open('mdAll.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(mdList))