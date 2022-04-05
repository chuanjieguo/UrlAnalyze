import redis
import sys
import getopt
pool = redis.ConnectionPool(decode_responses=True)
r = redis.Redis(host='127.0.0.1', port=6379, decode_responses=True)

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

param = get_argv(sys.argv[1:])
key = param.get('key', '')
if key[-1:] != '*':
    key = key + '*'
bg = 0
total = 0
while True:
    rt, dl = r.scan(bg, key, 10000)
    if len(dl) > 0:
        total += len(dl)
        # for d in dl:
        #     v = r.hgetall(d)
        #     print(v)
    if rt == 0:
        break
    bg = rt

print("{} total count:{}".format(key, total))