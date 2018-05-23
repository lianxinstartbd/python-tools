#!/usr/bin/env python
#-*-coding: utf-8 -*-
"""
  @FileName : webpage_save.py
  @Author : lianxin
  @CreateTime : 2016-12-01 20:10
  @Last modified : 2016-12-03 12:10
  @Description : main function
"""
import os
import re
import urllib

class WebPageSave(object):
    """
        summary: This class realize webpage_save.
    """
    def __init__(self, logger):
        """
            summary: init the config_file.
            Attributes:
                logger: A handler of logger.
        """
        self.log = logger
        
    def check_url_pattern(self, pattern, url):
        """
            summary: check the url if match pattern
            Attributes:
                pattern: url pattern.
                url: the url will be matched
            Returns:
                return True or False of check result.
        """
        pattern = re.compile(pattern)
        if re.search(pattern, url) is not None:
            self.log.warning("The url: %s match pattern" % url)
            return True
        else:
            self.log.warning("The url: %s not match pattern" % url)
            return False
            
    def save_url(self, url, output_directory):
        """
            summary: save the url
            Attributes:
                url: the url need to save.
            Returns:
                return True or False of save.
        """
        try:
            file_name = urllib.quote_plus(url)
            output_path = output_directory
            if False == os.path.exists(output_path):
                os.makedirs(output_path)
            fout = open('%s/%s' % (output_path, file_name), "w")
        except IOError as e:
            self.log.warning("Save url: %s failed!" % url)
            return False
       
        page = urllib.urlopen(url).read()
        fout.write(page)
        fout.close()
        self.log.info("Save url: %s success!" % url)
        return True
    
    
    
