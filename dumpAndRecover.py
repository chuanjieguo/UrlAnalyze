# -*- coding: utf-8 -*-
# @Time    : 2021-07-08 09:46
# @Author  : chuanjieguo
# @Mail    : chuanjieguo@139.com
# 从tpl文件中恢复或将数据备份至tpl文件
import pickle
import re
import getopt
import sys
import os
import redis
import time
import random

debug = False
index = 0
r = redis.Redis(host='127.0.0.1', port=6379, decode_responses=True)

def get_argv(argv):
    """
    根据命令行输入，获取相关参数
    :param argv: 命令行数组
    :return:
    """
    dic = {}
    info = '-h <help> -f <file> -k <key> -t <type>\nExample: -f example.tpl\n-k qq: -t set/value -o example.tpl'
    try:
        opts, args = getopt.getopt(argv, "h:f:k:t:o:", ["help=","file=", "key=", "type=", "out="])
    except getopt.GetoptError:
        print('Error: ' + info)
    if len(opts) == 0:
        print('please input parameter\n' + info)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print(info)
            sys.exit()
        elif opt in ("-f", "--file"):
            dic['file'] = arg
        elif opt in ("-k", "--key"):
            dic['key'] = arg
        elif opt in ("-t", "--type"):
            dic['type'] = arg
        elif opt in ("-o", "--out"):
            dic['out'] = arg
    return dic

def log(str):
    global debug
    if debug:
        with open('log.txt', 'a+', encoding='utf-8') as f:
            f.write(str + '\n')
param = get_argv(sys.argv[1:])
f = param.get('file', '')
key = param.get('key', '')
type = param.get('type', '')
out = param.get('out', '')

bg = 0
total = 0
wdic = {}
if f == '':
    if key != '':
        if out == '':
            out = "{}.tpl".format(key.strip(":"))
        if key[-1:] != '*':
            key = key + '*'
        i = 0
        while True:
            rt, dl = r.scan(bg, key, 10000)
            if len(dl) > 0:
                for d in dl:
                    if type == 'value':
                        v = r.get(d)
                    else:
                        v = r.hgetall(d)
                    wdic[d] = v
                    i += 1
            if rt == 0:
                break
            bg = rt
        print("Dump {} {}".format(i, key))
        pickle.dump(wdic, open(out, 'wb'), -1)
else:
    wdic = pickle.load(open(f, 'rb')) #type: dict
    i = 0
    for k, v in wdic.items():
        if isinstance(v, dict):
            r.hmset(k, v)
        else:
            r.set(k, v)
        i += 1
    print("Recover {} {}".format(i, f))
