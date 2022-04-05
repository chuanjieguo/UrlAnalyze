from CrawlerTools import WebType, PageType, Page, CrawlerTools
import time
from datetime import datetime
import json

tools = CrawlerTools(printTag=True)


def log(txt, path=''):
    if path == '':
        path = "log-" + time.strftime('%Y%m%d') + ".txt"
    with open(path, "a+", encoding="utf-8") as f:
        str = "{0} {1}\r\n".format(datetime.now().strftime("%H:%M:%S"), txt)
        f.write(str)

with open('list.txt', 'r', encoding='utf-8') as f:
    resList = []
    for line in f:
        line = line.strip()
        res = tools.checkHost(line)
        resList.append(res)
        log("{}\t{}".format(line, len(res)))
        if len(resList) % 10 == 0:
            with open('json_{}.txt'.format(time.strftime('%Y%m%d')), 'w', encoding='utf-8') as f:
                json.dump(resList, f, ensure_ascii=True)
