#!/usr/bin/env python
#-*-coding: utf-8 -*-
"""
  @FileName : logger.py
  @Author : wangqun02(wangqun02@baidu.com)
  @CreateTime : 2016-11-24 20:10
  @Last modified : 2016-11-26 10:10
  @Description : logger
"""
import os
import logging.handlers
    
LOGLEVEL_MAP = {
      'INFO': logging.INFO,
      'WARNING': logging.WARNING,
      'ERROR': logging.ERROR,
   }
   
class Logger(object):
    """
        summary: The Looger class, use to record the runing details.
    """
    def __init__(self, logfile, level='INFO', format="[%(levelname)s] [%(asctime)s] %(message)s",dateformat="%m-%d %H:%M:%S"):
        """
            summary: init the logger.
            Attributes:
                log_file: the file that log has saved .
        """
        dir = os.path.dirname(logfile)
        if not os.path.isdir(dir):
            os.makedirs(dir)
            
        self.logger = logging.getLogger()
        self.level = LOGLEVEL_MAP['INFO']
        if level in LOGLEVEL_MAP.keys():
            self.level = LOGLEVEL_MAP[level]
        self.logger.setLevel(self.level)
        
        formatter = logging.Formatter(format, dateformat)
        self.handler = logging.handlers.TimedRotatingFileHandler(logfile + ".log", 'D', 1, 10)
        self.handler.setFormatter(formatter)
        self.handler.setLevel(self.level)
        self.logger.addHandler(self.handler)
                
    def info(self, msg):
        """INFO level
        """
        self.logger.info(msg)

    def warning(self, msg):
        """WARNING level
        """
        self.logger.warning(msg)
   
    def error(self, msg):
        """ERROR level
        """
        self.logger.error(msg)
        
if '__main__' == __name__:
    log = Logger('./log/test', 'INFO')
    log.info('test info')
    log.warning('test warning')
    log.error('test error')