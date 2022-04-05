# -*- coding: utf-8 -*-
# @Time    : 2021-06-30 14:57
# @Author  : chuanjieguo
# @Mail    : chuanjieguo@139.com
import time
import getopt
import sys


def get_argv(argv):
    """
    根据命令行输入，获取相关参数
    :param argv: 命令行数组
    :return:
    """
    dic = {}
    info = '-h <help> -f <file> -o <outfile>'
    try:
        opts, args = getopt.getopt(argv, "h:f:o:", ["help=","file=", "out="])
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
        elif opt in ("-f", "--file"):
            dic['file'] = arg
        elif opt in ("-o", "--out"):
            dic['out'] = arg
    return dic
param = get_argv(sys.argv[1:])
path = param.get('file', '')
out = param.get('out', '')

print('before sleep {} {}'.format(path, out))
for i in range(6):
    time.sleep(5)
    print("sleeping {} {} {}".format(i, path, out))
print('after sleep {} {}'.format(path, out))