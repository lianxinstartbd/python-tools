#!/usr/bin/env python
#-*-coding: utf-8 -*-
"""
  @FileName : mini_spider.py
  @Author : lianxin
  @CreateTime : 2016-12-01 20:10
  @Last modified : 2016-12-05 12:10
  @Description : main function
"""
import threading
import time
import urllib2
import urlparse
import bs4

class MultiCrawler(object):
    """
        summary: This class realize crawl url.
    """
    def __init__(self, interval, timeout, max_depth, logger, url_depth, url_visited):
        """
            summary: init the multicrawler.
            Attributes:
                interval, timeout, max_depth, logger, url_depth, url_visited.
        """
        self.crawl_interval = interval
        self.crawl_timeout = timeout
        self.max_depth = max_depth
        self.log = logger
        self.multi_crawler_lock = threading.Lock()
        self.url_depth = url_depth
        self.url_visited = url_visited
    
    def multi_crawler(self, url):
        """
            summary: realize the multicrawler.
            Attributes:
                url: the url need to crawl.
            Returns:
                ret_urls : the urls have crawled
        """
        ret_urls = []
        if self.url_depth[url] <= int(self.max_depth):
            self.multi_crawler_lock.acquire()
            '''
            if url has visited, return none
            '''
            if url in self.url_visited:
                self.multi_crawler_lock.release()
                return None
            self.url_visited.append(url)
            self.multi_crawler_lock.release()
            ret = self.run(url, self.crawl_timeout)
            if ret['status']:
                for url_link in ret['urls']:
                    if url_link not in self.url_visited:
                        ret_urls.append(url_link)
                        self.multi_crawler_lock.acquire()
                        self.url_depth[url_link] = self.url_depth[url] + 1
                        self.multi_crawler_lock.release()
                time.sleep(int(self.crawl_interval))
                return ret_urls
        return None
    
    def run(self, url, timeout=1.0):
        """
            summary: realize the multicrawler.
            Attributes:
                url: the url need to crawl.
                timeout: crawl timeout
            Returns:
                The status and the urls have been crawled
        """
        self.url = url
        self.base_url = ""
        ret = {}
        ret['urls'] = []
        try:
            self.log.info("Start to crawl the url: %s" % (self.url))
            req = urllib2.Request(self.url)
            page = urllib2.urlopen(req, data=None, timeout=float(timeout))
            html = page.read()
            soup = bs4.BeautifulSoup(html, from_encoding="gbk")

            for meta in soup.find_all('meta'):
                content = meta.get('content')
                if content is not None and "url=" in content:
                    res = content.split("url=")[1]
                    ret['urls'].append(res.encode('utf-8'))
                    self.log.info("The crawled url: %s" % res)
            
            for base in soup.find_all('base'):
                if self.base_url == "":
                    self.base_url = base.get('href')
                    if self.base_url == "_blank":
                        self.base_url = ""
            
            for link in soup.find_all('a'):
                href = link.get('href')
                if href is not None:
                    if href.startswith('http', 0):
                        res = href
                    elif href.startswith('javascript', 0) and 'href' in href:
                        href = href.split('="')[1].strip('\"')
                        res = urlparse.urljoin(self.url, "%s%s" % (self.base_url, href))
                    else:
                        res = urlparse.urljoin(self.url, "%s%s" % (self.base_url, href))
                    ret['urls'].append(res.encode('utf-8'))
                    self.log.info("The crawled url: %s" % res)

            for img in soup.find_all('img'):
                res = urlparse.urljoin(self.url, "%s%s" % (self.base_url, img.get('src')))
                ret['urls'].append(res.encode('utf-8'))
                self.log.info("The crawled url: %s" % res)

            ret['status'] = True
            return ret
        except IOError as e:
            ret['status'] = False
            self.log.error("Url: %s has IOError: %s" % (str(self.url), str(e)))
            return ret
        except AttributeError as e:
            ret['status'] = False
            self.log.error("Url: %s has AttributeError: %s" % (str(self.url), str(e)))
            return ret
        except ValueError as e:
            ret['status'] = False
            self.log.error("Url: %s has ValueError: %s" % (str(self.url), str(e)))
            return ret
    
    
    
