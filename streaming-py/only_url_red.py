#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
only_url
"""
import sys
current_furl = None
current_objurl = None
current_count = 0
furl = None
for line in sys.stdin:
    if line != '\n':
        line = line.strip()
        furl, objurl = line.split('\t', 1)
        furl = furl.strip()
        objurl = objurl.strip()
        if current_furl == furl:
            current_objurl = objurl
        else:
            if current_furl:
                print '%s\t%s' % (current_furl, current_objurl)
            current_furl = furl
            current_objurl = objurl
if current_furl == furl:
    print '%s\t%s' % (current_furl, current_objurl)
