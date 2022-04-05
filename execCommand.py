# -*- coding: utf-8 -*-
# @Time    : 2021-06-30 14:53
# @Author  : sanclark
# @Mail    : sanclark@qq.com
import os
import subprocess

if os.path.exists('cmd.txt'):
    with open('cmd.txt', 'r', encoding='utf-8') as f:
        for l in f:
            ret = subprocess.call(l, shell=True)
            print("{} {}".format(ret, l))
else:
    print('No cmd.txt found!')