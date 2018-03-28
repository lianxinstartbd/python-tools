#!/usr/bin/env python
#-*-coding: utf-8 -*-
"""
  @FileName : config_load.py
  @Author : lianxin
  @CreateTime : 2016-11-25 20:10
  @Last modified : 2016-12-03 12:10
  @Description : load config and urls
"""
import sys
import os
import ConfigParser

class ConfigLoad(object):
    """
        summary: This class load the config_file.
    """
    def __init__(self, logger):
        """
            summary: init the config_file.
            Attributes:
                logger: A handler of logger.
        """
        self.conf_file = ""
        self.config = {}
        self.log = logger
        self.url_depth = {}
        self.url_queue = []
    
    def load_config(self, conf_file):
        """
            summary: load config_from conf_file.
            Attributes:
                conf_file: the config_file of mini_spider.
            Rerurns:
                the configs from conf_file.
        """
        self.conf_file = conf_file
        conf_parser = ConfigParser.ConfigParser()
        conf_parser.read(self.conf_file)
        self.log.info("Start to load config file: %s" % (self.conf_file))
        if 'spider' in conf_parser.sections():
            conf_options = ('url_list_file', 'output_directory', 'max_depth', 'crawl_interval', 'crawl_timeout', 'target_url', 'thread_count')
            if set(conf_options).issubset(set(conf_parser.options('spider'))):
                conf = {}
                for key, value in conf_parser.items('spider'):
                    conf[key] = value
                self.log.info("load config success!")
                return conf
            else:
                conf_empty = set(conf_options) - set(conf_parser.options('spider'))
                self.log.error("conf empty: %s" % conf_empty)
                sys.exit(1)
        else:
            self.log.error("Cannot find spider in %s" % self.conf_file)
            sys.exit(1)
            
    def load_urls_from_file(self, url_list_file):
        """
            summary: laod url from urls.
            Attributes:
                file: the url_file of mini_spider.
            Returns:
                the urls from the url_file.
        """
        if False == os.path.exists(url_list_file):
            self.log.error("The file: %s not exist!" % url_list_file)
            sys.exit(1)
        
        try:
            fp = open(url_list_file)
        except IOError as e:
            self.log.error("Cannot open the file: %s" % url_list_file)
            sys.exit(1)
    
        urls = []
        for url in fp:
            urls.append(url.split('\n')[0])
        fp.close()
        self.log.info("Load urls success!")
        return urls
    
    
    
