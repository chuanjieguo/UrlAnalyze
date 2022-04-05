# -*- coding: utf-8 -*-
# @Time    : 2021-07-13 15:22
# @Author  : sanclark
# @Mail    : sanclark@qq.com
import re
from IpSearch import IpSearch

def ip2Dec(ip):
    '''
    字符IP转十进制
    :param ip:
    :return:
    '''
    dec_value = 0
    v_list = ip.split('.')
    v_list.reverse()
    t = 1
    for v in v_list:
        dec_value += int(v) * t
        t = t * (2 ** 8)
    return dec_value


def dec2Ip(dec):
    '''
    十进制转字符IP
    :param dec:
    :return:
    '''
    ip = ''
    t = 2 ** 8
    for _ in range(4):
        v = dec % t
        ip = '.' + str(v) + ip
        dec = dec // t
    ip = ip[1:]
    return ip

def checkIp(ip):
    '''
    检测IP是否是合法IP，如果是，返回十进制，否则返回0
    :param ip:
    :return:
    '''
    if re.match(r"^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$",
                        ip) is None:
        return 0
    dec = ip2Dec(ip)
    if dec < 16777217 or 167772160 < dec < 184549375 or 2130706430 < dec < 2147483649 or 2886729728 < dec < 2887778303 or 3232235520 < dec < 3232301055 or dec > 4294967294:
        return 0
    return dec

finder = IpSearch("qqzeng-ip-3.0-ultimate.dat")
def checkOutside(ip):
    '''
    检测IP是否是国外的，如果是，返回True，否则返回False
    :param ip:
    :return:
    '''
    global finder
    try:
        ipr = finder.lookup(ip)
        # ipr = "亚洲|中国|江苏|南京|秦淮|114DNS|320104|China|US|118.79815|32.01112"
    except Exception as e:
        return False
    ipes = ipr.split('|')
    if len(ipes) == 11 and ipes[8] != 'CN':
        return True
    else:
        return False