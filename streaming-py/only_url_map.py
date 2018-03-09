#!/bin/python
# coding=utf-8
import sys
import json
import random
import os
src_file = os.environ['map_input_file']
cnt = 0
for line in sys.stdin:
    if line != '\n':
        line = line.strip()
        ## From furl_contsign file
        if 'test1' in src_file:
            print '%s\t%s' % (furl, objurl)
        if 'test2' in src_file:
            print '%s\t%s' % (furl, objurl)
