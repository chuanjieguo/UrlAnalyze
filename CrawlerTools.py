# -*- coding: utf-8 -*-
# @Time    : 2021-05-18 17:13
# @Author  : chuanjieguo
# @Mail    : chuanjieguo@139.com
from selenium import webdriver
from enum import Enum
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.remote.webelement import WebElement
import time
from datetime import datetime
import requests
import re
from selenium.webdriver.chrome.options import Options
import lxml.html as html
from urllib import parse
from DnsPostfix import getMainDomain, checkDns
import jieba
import random
import pickle
import traceback
import sys
import os

class WebType(Enum):
    '''
    驱动类型
    '''
    IE = 0
    EDEG = 1
    CHROME = 2
    FIREFOX = 3


class PageType(Enum):
    '''
    灰度识别结果
    '''
    SAFE = 1
    UNKNOWN = 2
    GREY = 3
    SEQING = 4
    BOCAI = 5


class Page:
    def __init__(self, md, url, title, description, keywords, body, linkList, src, headwords, bodywords, res):
        self.md = md
        self.url = url
        self.title = title
        self.description = description
        self.keywords = keywords
        self.body = body
        self.linkList = linkList
        self.src = src
        self.headwords = headwords
        self.bodywords = bodywords
        self.res = res

class CrawlerTools:
    def __init__(self, type=WebType.CHROME, timeOut=30, findWait=1, kuPath='allwords.txt', keyPath='keywords.txt', printTag=True, white='white.txt', black='black.txt', restartInterval=3600):
        """
        初始化函数
        :param type:
        :param cookies:
        :param globalWait:
        :param userPath: chrome的用户目录文件夹
        :param kuPath:词库路径
        :param keyPath:关键字及对应分类的文件路径
        """
        self.type = type
        self.timeOut = timeOut
        self.findWait = findWait
        self.kuPath = kuPath
        self.keyPath = keyPath
        self.browser = None

        # 加载txt文件
        self.keywords = {}
        jieba.load_userdict(self.kuPath)
        with open(self.keyPath, 'r', encoding='utf-8') as f:
            for line in f:
                ls = line.strip().split('\t')
                if len(ls) != 2:
                    continue
                self.keywords[ls[0]] = self.toType(ls[1])

        self.webList = []
        self.printTag = printTag
        self.whiteSet = set()
        self.blackSet = set()
        self.white = white
        self.black = black
        self.loadList(self.blackSet, self.black)
        self.loadList(self.whiteSet, self.white)
        self.cur = time.time()
        self.restartWeb(True)
        self.restartTime = time.time()
        self.restartInterval = restartInterval


    def killTask(self, task, debug=False):
        try:
            result = os.popen(task)
            return result.read()
        except Exception as e:
            self.debugLog(sys._getframe().f_lineno, debug, traceback.format_exc())
            return ''



    def restartWeb(self, debug=False):
        try:
            if self.browser != None:
                self.browser.quit()
                self.debugLog(sys._getframe().f_lineno, debug, 'Restart ...')
                # self.debugLog(sys._getframe().f_lineno, debug, self.killTask('taskkill /F /IM chromedriver.exe'))
                # self.debugLog(sys._getframe().f_lineno, debug, self.killTask('taskkill /F /IM chrome.exe'))
        except Exception as e:
            self.debugLog(sys._getframe().f_lineno, debug, 'Restart ...{}'.format(traceback.format_exc()))

        if self.type == WebType.IE:
            self.browser = webdriver.Ie()
        elif self.type == WebType.EDEG:
            self.browser = webdriver.Edge()
        elif self.type == WebType.CHROME:
            options = Options()
            options.add_argument('--ignore-certificate-errors')
            # 启用无头模式，没有界面。
            options.add_argument('--headless')
            options.add_argument('--disable-gpu')
            options.add_argument('--no-sandbox')
            # if self.userPath != '':
            #     options.add_argument(self.userPath)
            self.browser = webdriver.Chrome(chrome_options=options)
        elif self.type == WebType.FIREFOX:
            self.browser = webdriver.Firefox()
        else:
            self.debugLog(sys._getframe().f_lineno, True, 'WebType Exception ...{}'.format(traceback.format_exc()))

        self.cookies = {}
        self.browser.set_page_load_timeout(self.timeOut)
        self.browser.set_script_timeout(self.timeOut)
        self.browser.implicitly_wait(self.findWait)


    def loadList(self, dstSet, path='white.txt'):
        '''
        加载黑名单或白名单
        :param dstSet: 需要重新加载的集合
        :param path: 文件路径
        :return:
        '''
        try:
            with open(path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    md = self.getMainDomain(line)
                    if md != None and md != '':
                        dstSet.add(md)
        except Exception as e:
            pass

    def checkBlack(self, host):
        '''
        检测host是否在黑名单
        :param host:
        :return:True or False
        '''
        md = self.getMainDomain(host)
        if md is not None and md != '':
            return md in self.blackSet
        return False

    def checkWhite(self, host):
        '''
        检测host是否在白名单
        :param host:
        :return:
        '''
        md = self.getMainDomain(host)
        if md is not None and md != '':
            return md in self.whiteSet
        return False

    def __del__(self):
        """
        析构函数，关闭代理服务器和浏览器
        :return:
        """
        try:
            self.browser.close()
        except Exception as e:
            # self.log("Exit error: " + repr(e))
            pass

    def log(self, txt, path=''):
        if path == '':
            path = "log-" + time.strftime('%Y%m%d') + ".txt"
        with open(path, "a+", encoding="utf-8") as f:
            str = "{0} {1}\r\n".format(datetime.now().strftime("%H:%M:%S"), txt)
            if self.printTag:
                print(str)
            f.write(str)

    def getDriver(self):
        """
        获取browser对象
        :return:
        """
        return self.browser

    def getCharset(self, txt):
        chs = re.search(r'charset=([^\'">\s]+)', txt, re.I)
        if chs:
            return chs.group(1)
        else:
            return 'utf-8'

    def debugLog(self, lineno, debug=True, txt=''):
        if debug:
            now = time.time()
            with open('debug{}.txt'.format(datetime.now().strftime("%m%d")), "a+", encoding="utf-8") as f:
                f.write("line {} {:.3f} {} {}\n".format(lineno, now-self.cur, datetime.now().strftime("%H:%M:%S.%f"), txt))
            self.cur = now


    def getInfoByDriverQuick(self, url, debug=False):
        '''
        获取网页的标题和描述文本(使用lxml解释器，用于加快速度）
        :param url: URL
        :return: host, 网页标题、描述, 关键字， 文本， 源代码, 网页链接集合
        '''
        interval = time.time() - self.restartTime
        if interval > self.restartInterval:
            self.restartWeb(debug)
            self.restartTime = time.time()
        driver = self.getDriver()
        title = des = keywords = txt = src = host = ''
        linkSet = set()
        self.cur = time.time()
        try:
            if not url.startswith("http://") and not url.startswith("https://"):
                if url.count('.') <= 1:
                    url = "http://www." + url
                else:
                    url = "http://" + url
            try:
                driver.get(url)
            except Exception as e: # TimeoutException
                pass
            src = driver.page_source
            p = parse.urlparse(driver.current_url)
            host = "{}://{}/".format(p.scheme, p.netloc)
            res = self.__getPageInfoByHtml(src, host, True, debug)
            if res is None:
                return False
            title, des, keywords, txt, linkSet = res
            if title == '' and des == '' and keywords == '' and txt == '' and len(linkSet) == 0:
                return False
            ifs = {}
            if re.search(r'<\s*iframe\s+', src, re.I):
                ifs = driver.find_elements_by_tag_name('iframe')
            elif re.search(r'<\s*frame\s+', src, re.I):
                ifs = driver.find_elements_by_tag_name('frame')
            for ife in ifs:
                try:
                    driver.switch_to.frame(ife)
                except Exception as e:
                    continue
                src += driver.page_source
                p = parse.urlparse(driver.current_url)
                host = "{}://{}/".format(p.scheme, p.netloc)
                tres = self.__getPageInfoByHtml(driver.page_source, host, False, debug)
                if tres is None:
                    continue
                txt += tres[3]
                linkSet.update(tres[4])
        except Exception as e:
            if "{}{}{}{}".format(title, des, keywords, txt).strip() == '':
                return False
        # self.debugLog(sys._getframe().f_lineno, debug)
        return host, title, des, keywords, txt, src, linkSet


    def getInfoByDriverLow(self, url, debug=False):
        '''
        获取网页的标题和描述文本（使用driver进行获取，比较慢）
        :param url: URL
        :return: host, 网页标题、描述, 关键字， 文本， 源代码, 网页链接集合
        '''
        driver = self.getDriver()
        title = des = keywords = txt = src = host = ''
        linkSet = set()
        #start = time.time()
        #print("line {} {:.3f} {}".format(sys._getframe().f_lineno, time.time() - start, datetime.now().strftime("%H:%M:%S.%f"))) if debug else ''
        try:
            if not url.startswith("http://") and not url.startswith("https://"):
                if url.count('.') <= 1:
                    url = "http://www." + url
                else:
                    url = "http://" + url
            try:
                driver.get(url)
            except Exception as e: # TimeoutException
                pass
            src += driver.page_source
            host = driver.current_url
            ifs = {}
            if re.search(r'<\s*iframe\s+', src, re.I):
                ifs = driver.find_elements_by_tag_name('iframe')
            res = self.__getPageInfoByDriver(driver, True)
            if res is None:
                return False
            title, des, keywords, txt, linkSet = res
            for ife in ifs:
                try:
                    driver.switch_to.frame(ife)
                except Exception as e:
                    continue
                host = driver.current_url
                src += driver.page_source
                tres = self.__getPageInfoByDriver(driver, False)
                if tres is None:
                    continue
                txt += tres[3]
                linkSet.update(tres[4])
        except Exception as e:
            if "{}{}{}{}".format(title, des, keywords, txt).strip() == '':
                return False
        return host, title, des, keywords, txt, src, linkSet


    def getInfoByApi(self, url, timeout=30):
        '''

        :param url:
        :param timeout:
        :return: host, 网页标题、描述, 关键字， 文本, 源代码
        '''
        description = keywords = title = src = ''
        linkSet = set()
        header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36'
            }
        try:
            if not url.startswith("http://") and not url.startswith("https://"):
                url = "http://" + url
            resp = requests.get(url, timeout=timeout, headers=header)

            if resp.text is None or resp.text == '':
                return False
            resp.encoding = self.getCharset(resp.text)
            # bs = BeautifulSoup(resp.text, 'lxml')
            p = parse.urlparse(resp.url)
            host = "{}://{}/".format(p.scheme, p.netloc)
            res = self.__getPageInfoByHtml(resp.text, host, True)
            if res is None:
                return False
            return host, res[0], res[1], res[2], res[3], resp.text, res[4]
        except Exception as e:
            #print(repr(e))
            return False


    def __getPageInfoByDriver(self, driver, head=True, debug=False):
        '''
        根据driver的源代码，获取页面的相关信息
        :param driver:
        :param head:
        :return: title, description, keywords, txt.strip(), linkSet，如果失败，返回None
        '''
        if driver is None: #type: webdriver
            return None
        try:
            src = driver.page_source
            linkSet = set()
            title = des = keywords = txt = ''
            if head:
                metas = driver.find_elements_by_tag_name('meta')
                for meta in metas:  # type: WebElement
                    if meta.get_attribute('name').lower() == 'description':
                        des = meta.get_attribute('content')
                    if meta.get_attribute('name').lower() == 'keywords':
                        keywords = meta.get_attribute('content')
                title = driver.title
            links = driver.find_elements_by_tag_name('a')
            for link in links:
                try:
                    lt = link.get_attribute('href')
                except Exception as e:
                    continue
                if lt is not None and lt != '' and lt.startswith('http'):
                    linkSet.add(lt)

            doc = html.fromstring(src)
            ignore_tags = ('script', 'noscript', 'style')
            for elt in doc.body.iterdescendants():
                if elt.tag in ignore_tags:
                    continue
                text = re.sub(r"<[^>]+>", '', elt.text or '')
                tail = re.sub(r"<[^>]+>", '', elt.tail or '')
                words = ' '.join((text, tail)).strip()
                if words:
                    txt += ' ' + words    #.encode('utf-8')
        except Exception as e:
            self.debugLog(sys._getframe().f_lineno, debug, traceback.format_exc())
            if "{}{}{}{}".format(title, des, keywords, txt).strip() == '':
                return None
        return title, des, keywords, txt.strip(), linkSet


    def __getPageInfoByHtml(self, src, host, head=True, debug=False):
        '''
        根据页面的源代码，获取页面的相关信息
        :param txt:
        :param host:
        :return: title, description, keywords, txt.strip(), linkSet，如果失败，返回None
        '''
        if src is None or src == '':
            return None
        linkSet = set()
        title = description = keywords = ''
        try:
            doc = html.fromstring(src)
            for link in doc.xpath('//a/@href'):
                if link.lower().startswith("http"):
                    linkSet.add(link)
                elif link.startswith('.'):
                    linkSet.add(host + link.strip('./'))
                elif link.startswith('/'):
                    linkSet.add(host + link.strip('/'))
                elif link.find(":") >= 0:
                    continue
                else:
                    linkSet.add(host + link)
            ignore_tags = ('script', 'noscript', 'style')
            if head:
                for elt in doc.head.iterdescendants():
                    if elt.tag in ignore_tags:
                        continue
                    if title == '' and elt.tag == 'title':
                        title = elt.text or ''
                    if elt.tag == 'meta':
                        name = elt.xpath('./@name')[0] if len(elt.xpath('./@name')) > 0 else None
                        content = elt.xpath('./@content')[0] if len(elt.xpath('./@content')) > 0 else ''
                        if name is not None and name.lower() == 'keywords':
                            keywords = content
                        if name is not None and name.lower() == 'description':
                            description = content
            txt = ''
            for elt in doc.body.iterdescendants():
                if elt.tag in ignore_tags:
                    continue
                text = re.sub(r"<[^>]+>", '', elt.text or '')
                tail = re.sub(r"<[^>]+>", '', elt.tail or '')
                words = ' '.join((text, tail)).strip()
                if words:
                    txt += ' ' + words  # .encode('utf-8')
        except Exception as e:
            self.debugLog(sys._getframe().f_lineno, debug, traceback.format_exc())
            if "{}{}{}{}".format(title, description, keywords, txt).strip() == '':
                return None
        return title, description, keywords, txt.strip(), linkSet

    def getMainDomain(self, host):
        '''
        获取url的主域
        :param host:
        :return:如果是非法域名，则返回None
        '''
        if host is None:
            return None
        if not host.startswith('http'):
            host = 'http://' + host
        try:
            hres = parse.urlparse(url=host,scheme='http',allow_fragments=True)
            md = hres.hostname
            ri = md.rfind('.')
            if ri < 0:
                return None
            pfix = md[ri:]
            if not checkDns(pfix):
                return None
            return getMainDomain(md)
        except Exception as e:
            return None

    def getUrlOutSide(self, host, linkSet):
        '''
        获取外域的域名
        :param host:
        :param linkSet:
        :return:
        '''
        if host is None:
            return None
        ls = []
        hres = parse.urlparse(url=host,scheme='http',allow_fragments=True)
        md = self.getMainDomain(hres.hostname)
        if md is None:
            return ls
        for link in linkSet:
            lres = parse.urlparse(url=link,scheme='http',allow_fragments=True)
            lmd = self.getMainDomain(lres.hostname)
            if lmd is None:
                continue
            if md != lmd:
                ls.append(link)
        return ls

    def toType(self, txt):
        '''
        将文本转化为页面类型
        :param txt:
        :return:
        '''
        if txt == 'SEQING':
            return PageType.SEQING
        if txt == 'BOCAI':
            return PageType.BOCAI
        return PageType.UNKNOWN


    def getWords(self, txt):
        '''
        匹配分词的类型，输出匹配的词语列表及其对应的类型
        :param txt:
        :return:
        '''
        words = jieba.lcut(txt)
        wSet = set()
        res = {}
        for word in words:
            wSet.add(word)
        for word in wSet:
            uWord = word.upper()
            if uWord in self.keywords:
                res[uWord] = self.keywords[uWord]
        return res

    def getType(self, res, th=3):
        '''
        根据关键词扫描结果，获取最后的识别结果
        :param res:
        :param th:
        :return:
        '''
        if len(res) < 1:
            return PageType.SAFE
        tDic = {}
        tDic.keys()
        for v in res.values():
            tDic[v] = tDic.get(v, 0) + 1
        tSorted = sorted(tDic.items(), key=lambda ie: ie[1], reverse=True)
        if tSorted[0][1] >= th:
            return tSorted[0][0]
        elif len(res) >= th:
            return PageType.GREY
        else:
            return PageType.UNKNOWN

    def getTopUrl(self, md):
        '''
        这儿根据自己的实际情况，获取该主域对应的top1 url
        :param md:
        :return:
        '''
        return ''

    def checkHost(self, md, debug=False):
        '''
        对主域名进行爬虫，并完成关键字提取、灰度识别流程
        :param md: 主域
        :return: 返回识别结果多元组
        '''
        res = self.getInfoByDriverQuick(md, debug)
        if res == False:
            url = self.getTopUrl(md)
            if url != '':
                res = self.getInfoByDriverQuick(md, debug)
        self.cur = time.time()
        self.debugLog(sys._getframe().f_lineno, debug)
        if res != False:
            host, title, des, key, content, src, linkSet = res
            head = "{} {} {}".format(title, des, key)

            resType = PageType.UNKNOWN
            hType = PageType.UNKNOWN
            bType = PageType.UNKNOWN
            hWords = {}
            bWords = {}
            if head.strip() != '':
                hWords = self.getWords(head)
                if len(hWords) < 1:
                    hType = PageType.SAFE
                else:
                    hType = self.getType(hWords, 2)
                resType = hType
            if hType.value <= PageType.UNKNOWN.value:
                if content.strip() != '':
                    bWords = self.getWords(content)
                    if len(bWords) < 1:
                        bType = PageType.SAFE
                    else:
                        bType = self.getType(bWords, 3)
                resType = bType
            self.debugLog(sys._getframe().f_lineno, debug)
            ls = self.getUrlOutSide(host, linkSet)
            resDic = {
                'host': host,
                'title': title,
                'description': des,
                'keywords': key,
                'body': content,
                'headtype': hType.value,
                'headwords': ",".join(hWords.keys()),
                'bodyType': bType.value,
                'bodywords': ",".join(bWords.keys()),
                'restype': resType.value,
                'links': ','.join(ls)
            }
            self.debugLog(sys._getframe().f_lineno, debug)
            self.webList.append(Page(md, host, title, des, key, content, ls, src, hWords, bWords, resType.value))
            self.debugLog(sys._getframe().f_lineno, debug)
            return resDic
        else:
            self.log("{} page is None".format(url))
        self.debugLog(sys._getframe().f_lineno, debug)
        return {}


    def dumpWebList(self, path=''):
        '''
        将webList dump至文件
        :return:
        '''
        if path == '':
            rint = random.randint(100, 999)
            path = 'webList_{}.tpl'.format(rint)
        pickle.dump(self.webList, open(path, 'wb'), -1)
