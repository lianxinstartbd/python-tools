#!/usr/bin/env python
#-*-coding: utf-8 -*-
"""
  @FileName : mini_spider.py
  @Author : lianxin
  @CreateTime : 2016-11-24 20:10
  @Last modified : 2016-12-03 12:10
  @Description : main function
"""
import sys
import os.path
import getopt
import time
import threading
from multiprocessing import dummy
import config_load
import logger
import webpage_save
import multi_crawler

def minispider_usage(self):
    print "mini_spider.py usage:"
    print "-h: print help message"
    print "-v: print version message"
    print "-c: input one configuration file"
    
def minispider_version(self):
    print "mini_spider.py version 1.0"
    
class MiniSpider(object):
    """
        summary: This class realize mini_spider.
    """
    def __init__(self, conf_file):
        """
            summary: init the mini_spider.
            Attributes:
                conf_file: the config_file of mini_spider.
        """
        self.conf_file = conf_file
        self.config = {}
        self.log = logger.Logger('./log/mini_spider')
        self.urlqueue_lock = threading.Lock()
        self.multiple_spider_lock = threading.Lock()
        self.url_visited = []
        self.url_depth = {}
        self.url_queue = []
    
        
    def run(self):
        """summary: run the mini_spider.
           function:
               load the config_file;
               load the urls;
               create thread pool;
               multi_thread crawle the url;
               save the urls which matched
        """
        self.config_load = config_load.ConfigLoad(self.log)
        self.config = self.config_load.load_config(self.conf_file)
        url_file = os.path.abspath(os.path.dirname(self.conf_file)) + "/" + self.config['url_list_file']
        self.urls = self.config_load.load_urls_from_file(url_file)
        if self.urls == []:
            return []
        
        self.url_queue = self.urls
        for url in self.url_queue:
            self.url_depth[url] = 0
            print self.url_depth
        pool = dummy.Pool(int(self.config['thread_count']))
        
        self.multi_crawler = multi_crawler.MultiCrawler(self.config['crawl_interval'], self.config['crawl_timeout'], self.config['max_depth'], self.log, self.url_depth, self.url_visited)
        self.log.info("Start to crawl urls in the url_queue:%s" % (self.url_queue))
        while self.url_queue != []:
            rets = pool.map(self.multi_crawler.multi_crawler, self.url_queue)
            self.url_queue = []
            for ret in rets:
                if ret is not None:
                    self.urlqueue_lock.acquire()
                    self.url_queue.extend(ret)
                    self.urlqueue_lock.release()
        pool.close()
        pool.join()
        self.webpage_save = webpage_save.WebPageSave(self.log)
        for url in self.url_visited:
            if self.webpage_save.check_url_pattern(self.config['target_url'], url):
                self.log.info("Match url: %s" % url)
                if self.webpage_save.save_url(url, self.config['output_directory']):
                    self.log.info("success save url: %s" % url)
                else:
                    self.log.error("Failed to save url: %s" % (url))
        self.log.info("End to spider!")
        
if __name__ == '__main__':
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hvc:")
    except getopt.GetoptError,err:
        minispider_usage()
        sys.exit(1)
    for o, a in opts:
        if o in "-h":
            minispider_usage()
            sys.exit(0)
        elif o in "-v":
            minispider_version()
            sys.exit(0)
        elif o in "-c":
            if os.path.exists(a):
                mini_spider = MiniSpider(a)
                mini_spider.run()
            else:
                print "The config_file is not exists!"
                minispider_usage()
                sys.exit(1)
        else:
            print "mini_spider.py need a option "
            minispider_usage()
            sys.exit(0)

