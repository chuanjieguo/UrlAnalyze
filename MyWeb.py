from selenium import webdriver
from enum import Enum
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
from selenium.webdriver.remote.webelement import WebElement
import json
import time
from datetime import datetime
import requests
import re
import os
from browsermobproxy import Server
from selenium.webdriver.chrome.options import Options
import random
from configparser import ConfigParser
import sys
import lxml.html as html
from bs4 import BeautifulSoup, element
from urllib import parse
from DnsPostfix import getMainDomain, checkDns

class WebType(Enum):
    IE = 0
    EDEG = 1
    CHROME = 2
    FIREFOX = 3


class MyWeb:
    def __init__(self, type=WebType.CHROME, userPath='', proxyPath='', timeOut=30,):
        """
        初始化函数
        :param type:
        :param cookies:
        :param globalWait:
        :param userPath: chrome的用户目录文件夹
        :param proxyPath: 代理browsermob-proxy.bat的路径
        """
        self.server = None
        self.proxy = None
        if type == WebType.IE:
            self.browser = webdriver.Ie()
        elif type == WebType.EDEG:
            self.browser = webdriver.Edge()
        elif type == WebType.CHROME:
            options = Options()
            options.add_argument('--ignore-certificate-errors')
            # 启用无头模式，没有界面。
            options.add_argument('--headless')
            if userPath != '':
                options.add_argument(userPath)
            else:
                self.log("No user directory to be added.")
            if proxyPath != '' and os.path.isfile(proxyPath):
                self.startProxy(proxyPath)
                options.add_argument('--proxy-server={0}'.format(self.proxy.proxy))
            else:
                self.log("No proxy to be started.")
            self.browser = webdriver.Chrome(chrome_options=options)
        elif type == WebType.FIREFOX:
            self.browser = webdriver.Firefox()
        else:
            raise Exception("Not support this web browser.")
        self.cookies = {}
        # self.browser.implicitly_wait(globalWait)
        self.type = type
        self.timeOut = timeOut

    def __del__(self):
        """
        析构函数，关闭代理服务器和浏览器
        :return:
        """
        try:
            if self.server is not None:
                self.server.stop()
            self.browser.close()
        except Exception as e:
            self.log("Exit error: " + repr(e))

    def startProxy(self, path):
        """
        启动代理服务器
        :param path: 代理browsermob-proxy.bat的路径
        :return:
        """
        try:
            self.server = Server(path)
            self.server.start()
            self.proxy = self.server.create_proxy()
        except Exception as e:
            self.log("Start proxy error: " + repr(e))

    def stopProxy(self):
        """
        关闭代理服务器
        :return:
        """
        try:
            self.server.stop()
        except Exception as e:
            self.log(repr(e))

    def startCap(self, name, capHeader=True, capContent=False, capBin=False):
        """
        启动抓包
        :param name: 抓包名文件名
        :param capHeader: 是否捕获请求头
        :param capContent: 是否捕获响应内容
        :param capBin: 是否捕获二进制内容
        :return:
        """
        if self.proxy is not None:
            op = {'captureHeaders': capHeader, 'captureContent': capContent, 'captureBinaryContent': capBin}
            self.proxy.new_har(name, options=op)
        else:
            self.log("No proxy for har.")

    def getUrl(self, uset=None, filter="", add=True):
        """
        从抓包文件中提取URL
        :param uset: 判断是否已经存在的url集合
        :param filter: url过滤器，支持正则表达式
        :param add: 是否将符合条件的url列表加入到set中
        :return: 返回符合条件的url列表
        """
        urls = []
        if self.proxy is None:
            self.log("No proxy started.")
            return urls
        result = self.proxy.har
        if result is None:
            self.log("No capture started.")
            return urls

        for entry in result['log']['entries']:
            nurl = ""
            url = entry['request']['url']
            if filter == "":
                nurl = url
            else:
                if re.search(filter, url) is not None:
                    nurl = url
            if nurl != "":
                if uset is None:
                    urls.append(nurl)
                else:
                    if not nurl in uset:
                        urls.append(nurl)
                        if add:
                            uset.add(nurl)
        return urls

    def getCookies(self, ele="", type=By.ID):
        """
        获取或刷新浏览器cookies，并返回字典
        :param ele:
        :return:
        """
        if ele != "":
            WebDriverWait(self.browser, timeout=300).until(
                EC.visibility_of_element_located((type, ele)))
        ck = self.browser.get_cookies()
        self.cookies.clear()
        for c in ck:
            self.cookies[c["name"]] = c["value"]
        self.log(json.dumps(self.cookies))
        return self.cookies

    def getCookiesValue(self, name, refresh=True):
        """
        根据cookies的名字获取cookies的值
        :param name:
        :param refresh:
        :return:
        """
        if refresh:
            self.getCookies()
        return self.cookies[name]

    def dumpCookies(self, path="cookies.txt"):
        """
        将cookies以json格式写入文件
        :param path:
        :return:
        """
        ck = self.getCookies()
        with open(path, "w", encoding="utf-8") as f:
            json.dump(ck, f, indent=4, ensure_ascii=False)

    def loadCookies(self, path="cookies.txt"):
        """
        从文件里面加载cookies
        :param path:
        :return:
        """
        with open(path, "r", encoding="utf-8") as f:
            self.cookies = json.load(f)

    def log(self, txt):
        with open("log-" + time.strftime('%Y%m%d') + ".txt", "a+", encoding="utf-8") as f:
            str = "{0} {1}\r\n".format(datetime.now().strftime("%H:%M:%S"), txt)
            print(str)
            f.write(str)

    def post(self, url, data="", headers={}, cookies={}):
        """
        处理post请求
        :param url:请求连接
        :param headers: 请求头字典
        :param data:请求体文本
        :param cookies:cookies字典
        :return:
        """
        if len(cookies) <= 0:
            cookies = self.cookies
        return requests.post(url, headers=headers, data=data, cookies=cookies)

    def get(self, url, headers={}, cookies={}):
        """
        处理get请求
        :param url:
        :param headers:
        :param cookies:
        :return:
        """

        if len(cookies) <= 0:
            cookies = self.cookies
        return requests.get(url, headers=headers, cookies=cookies)

    def getDriver(self):
        """
        获取browser对象
        :return:
        """
        return self.browser

    def download(self, dir, name, url, headers={}, cookies={}):
        """
        下载文件
        :param path:文件本地路径
        :param url:文件url
        :param headers:请求头
        :param cookies:请求cookies
        :return:
        """
        if dir != '' and not os.path.exists(dir):
            os.mkdir(dir)
        try:
            p = os.getcwd() + os.sep + dir + os.sep + name
            if not os.path.isfile(p):
                v = requests.get(url, headers=headers, cookies=cookies)
                with open(p, "wb") as f:
                    f.write(v.content)
                self.log("Getting " + url)
                self.log("Store in " + p)
        except Exception as e:
            self.log(repr(e))

    def fixName(self, name):
        """
        对文件名进行修正，避免非法
        :param name: 原文件名
        :return: 修正后的文件名
        """
        return re.sub(r"[\/\\\:\*\?\"\<\>\|]", '_', name)

    def getTitle(self, url):
        '''
        获取网页的标题和描述文本
        :param url: URL
        :return: 网页标题、描述tuple
        '''
        driver = self.getDriver()
        driver.set_page_load_timeout(self.timeOut)
        title = ''
        des = ''
        try:
            driver.get(url)
            WebDriverWait(driver, timeout=self.timeOut).until(
                EC.presence_of_element_located((By.XPATH, "/html/head/title")))
            title = driver.title
            metas = driver.find_elements_by_tag_name('meta')

            for meta in metas:  # type: WebElement
                if meta.get_attribute('name') == 'description':
                    des = meta.get_attribute('content')
                    break
        except:
            pass
        return title, des

    def getCharset(self, txt):
        chs = re.search(r'charset=([^\'">\s]+)', txt, re.I)
        if chs:
            return chs.group(1)
        else:
            return 'utf-8'

    def getInfoByDriver(self, url):
        '''
        获取网页的标题和描述文本
        :param url: URL
        :return: host, 网页标题、描述, 关键字， 文本， 源代码, 网页链接集合
        '''
        driver = self.getDriver()
        driver.set_page_load_timeout(self.timeOut)
        title = ''
        des = ''
        keywords = ''
        txt = ''
        src = ''
        linkSet = set()
        host = ''
        try:
            if not url.startswith("http://") and not url.startswith("https://"):
                if url.count('.') <= 1:
                    url = "http://www." + url
                else:
                    url = "http://" + url
            driver.get(url)
            WebDriverWait(driver, timeout=self.timeOut).until(
                EC.presence_of_element_located((By.XPATH, "/html/head/title")))
            title = driver.title
            metas = driver.find_elements_by_tag_name('meta')
            for meta in metas:  # type: WebElement
                if meta.get_attribute('name') == 'description':
                    des = meta.get_attribute('content')
                if meta.get_attribute('name') == 'keywords':
                    keywords = meta.get_attribute('content')

            links = driver.find_elements_by_tag_name('a')
            for link in links:
                lt = link.get_attribute('href')
                if lt is not None and lt != '' and lt.startswith('http'):
                    linkSet.add(lt)

            doc = html.fromstring(driver.page_source)
            src = driver.page_source
            host = driver.current_url
            ignore_tags = ('script', 'noscript', 'style')
            for elt in doc.body.iterdescendants():
                if elt.tag in ignore_tags:
                    continue
                text = re.sub(r"<[^>]+>", '', elt.text or '')
                tail = re.sub(r"<[^>]+>", '', elt.tail or '')
                words = ' '.join((text, tail)).strip()
                if words:
                    txt += ' ' + words    #.encode('utf-8')
            ifs = driver.find_elements_by_tag_name('iframe')
            for ife in ifs:
                driver.switch_to.frame(ife)
                links = driver.find_elements_by_tag_name('a')
                for link in links:
                    lt = link.get_attribute('href')
                    if lt is not None and lt != '' and lt.startswith('http'):
                        linkSet.add(lt)
                doc = html.fromstring(driver.page_source)
                src += driver.page_source
                for elt in doc.iterdescendants():
                    if elt.tag in ignore_tags:
                        continue
                    text = re.sub(r"<[^>]+>", '', elt.text or '')
                    tail = re.sub(r"<[^>]+>", '', elt.tail or '')
                    words = ' '.join((text, tail)).strip()
                    if words:
                        txt += ' ' + words  # .encode('utf-8')
        except Exception as e:
            #print(repr(e))
            if txt == '':
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
            doc = html.fromstring(resp.text)
            host = resp.url
            for link in doc.xpath('//a/@href'):
                if link.startswith("http"):
                    linkSet.add(link)
                elif link.startswith('.'):
                    linkSet.add(host + link.strip('./'))
                elif link.startswith('/'):
                    linkSet.add(host + link.strip('/'))
            src = resp.text
            ignore_tags = ('script', 'noscript', 'style')
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
            return host, title, description, keywords, txt.strip(), src, linkSet
        except Exception as e:
            #print(repr(e))
            return False


    def getMainDomain(self, host):
        '''
        获取域名的主域， host已经是去头去尾的域名
        :param host:
        :return:
        '''
        if host is None:
            return None
        ri = host.rfind('.')
        if ri < 0:
            return None
        pfix = host[ri:]
        if not checkDns(pfix):
            return None
        return getMainDomain(host)


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



