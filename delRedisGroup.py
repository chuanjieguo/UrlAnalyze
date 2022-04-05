# -*- coding: utf-8 -*-
# @Time    : 2021-06-21 14:42
# @Author  : sanclark
# @Mail    : sanclark@qq.com
import redis
import getopt
import sys

r = redis.Redis(host='127.0.0.1', port=6379)

def get_argv(argv):
    """
    根据命令行输入，获取相关参数
    :param argv: 命令行数组
    :return:
    """
    dic = {}
    info = '-h <help> -f <file>'
    try:
        opts, args = getopt.getopt(argv, "h:k:", ["help=","key="])
    except getopt.GetoptError:
        print('Error: ' + info)
        sys.exit(2)
    if len(opts) == 0:
        print('please input parameter\n' + info)
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print(info)
            sys.exit()
        elif opt in ("-k", "--key"):
            dic['key'] = arg
    return dic

def delGroup(r, group, batch=10000):
    if group[-1:] != '*':
        group = group + '*'
    bg = 0
    total = 0
    while True:
        rt, dl = r.scan(bg, group, 10000)
        print("deleting len {}".format(len(dl)))
        total += len(dl)
        if len(dl) > 0:
            r.delete(*dl)
        if rt == 0:
            break
        bg = rt
    print("total delete {}".format(total))

param = get_argv(sys.argv[1:])
key = param.get('key', '')
if key[-1:] != '*':
    key = key + '*'

delGroup(r, key)