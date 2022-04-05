from urllib.parse import urlparse
import redis
import time
from DnsPostfix import checkDns, getMainDomain
pool = redis.ConnectionPool(decode_responses=True)
r = redis.Redis(host='127.0.0.1', port=6379, password='gmcc@123')

with open('white.txt', 'r', encoding='utf-8') as f:
    for line in f:
        l = line.strip()
        md = getMainDomain(l)
        r.sadd("ku:white", md)

gList = [
    'ku:white',
    'ku:black'
]
for group in gList:
    c = r.scard(group)

    print("{} total count:{}".format(group, c))


print(r.sismember('ku:white', 'wenxiu365.com'))

print(r.sismember('ku:white', 'porn.com'))