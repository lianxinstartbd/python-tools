#!/usr/bin/env python
#-*-coding: utf-8 -*-
"""
  @FileName : spider_unittest.py
  @Author : lianxin
  @CreateTime : 2016-12-05 10:10
  @Last modified : 2016-12-05 20:10
  @Description : main function
"""
import unittest
import logger
import config_load
import multi_crawler
import webpage_save

class ConfigLoadTestCase(unittest.TestCase):
    
    def setUp(self):
        self.log = logger.Logger('./log/mini_spider_test')
        self.config_load = config_load.ConfigLoad(self.log)
        
    def tearDown(self):
        self.config_load = None

    def testLoadConfig(self):
        conf = self.config_load.load_config("./conf/spider.conf")
        self.assertEqual(len(conf),7)
        
    def testLoadUrl(self):
        url = self.config_load.load_urls_from_file("./conf/urls")
        self.assertEqual(url[0],"http://pycm.baidu.com:8081")   

class MultiCrawlerTestCase(unittest.TestCase):

    def setUp(self):
        self.log = logger.Logger('./log/mini_spider_test')
        self.multi_crawler = multi_crawler.MultiCrawler(1,1,3,self.log, {'http://pycm.baidu.com:8081/page2.html': 0}, [])
    
    def tearDown(self):
        self.multi_crawler = None
    
    def testMultiCrawler(self):
        urls = self.multi_crawler.multi_crawler("http://pycm.baidu.com:8081/page2.html")
        self.assertEqual(len(urls),2)
        
    def testRun(self):
        ret = self.multi_crawler.run("http://pycm.baidu.com:8081/page2.html")
        self.assertEqual(ret['status'], True)
        self.assertEqual(len(ret['urls']), 2)

class WebPageSaveTestCase(unittest.TestCase):
    
    def setUp(self):
        self.log = logger.Logger('./log/mini_spider_test')
        self.webpage_save = webpage_save.WebPageSave(self.log)
    
    def tearDown(self):
        self.webpage_save = None
    
    def testCheckUrlPattern(self):
        match_ret = self.webpage_save.check_url_pattern(".*.(htm|html)$", "http://pycm.baidu.com:8081/page2.html")
        self.assertEqual(match_ret, True)
    
    def testSaveUrl(self):
        save_ret = self.webpage_save.save_url("http://pycm.baidu.com:8081/page2.html", "./output")
        self.assertEqual(save_ret, True)
       
def  ConfigLoadTestSuite():
    
    suite = unittest.TestSuite()
    suite.addTest(ConfigLoadTestCase("testLoadConfig"))
    suite.addTest(ConfigLoadTestCase("testLoadUrl"))
    
def MultiCrawlerTestSuite():
    
    suite = unittest.TestSuite()
    suite.addTest(MultiCrawlerTestCase("testMultiCrawler"))
    suite.addTest(MultiCrawlerTestCase("testRun"))

def WebPageSaveTestSuite():
    
    suite = unittest.TestSuite()
    suite.addTest(WebPageSaveTestCase("testCheckUrlPattern"))
    suite.addTest(WebPageSaveTestCase("testSaveUrl"))

if __name__ == '__main__':
    unittest.main()
