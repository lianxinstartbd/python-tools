#!/bin/python
# coding=utf-8
import sys
import json
import random
import re
import os

#创建一个正则表达式匹配对象，从日志中提取host
reobj = re.compile(r"""(?xi)\A
                       [a-z][a-z0-9+\-.]*://                                # Scheme
                       ([a-z0-9\-._~%!$&'()*+,;=]+@)?                       # User
                       ([a-z0-9\-._~%]+                                     # Named or IPv4 host
                        |\[[a-z0-9\-._~%!$&'()*+,;=:]+\])                   # IPv6+ host
                   """)
cnt = 0
for line in sys.stdin:
    if line != '\n':
        line = line.strip()
        flds = line.split('\t')
        furl = flds[0]
        try:
            match = reobj.search(furl)
            #如果匹配到结果
            if match:
                host = match.group(2)
                print '%s\t%s' % (host, 1)
        except:
            continue

