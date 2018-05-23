#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
merge_url
"""

import sys

tag_a_host = None
tag_a_value = None
tag = None

for line in sys.stdin:
    if line != '\n':
        line = line.strip()
        host_tag, values = line.split(' ', 1)[1].split("\t", 1)
        host, tag = host_tag.rsplit("_", 1) 
        
        # reduce阶段的输入数据是map的输出
        # 相同reduce_index的数据被分到同一个桶里（相同url计算出的sign，reduce_index也是相同的），并且按照key进行排序（相同url是聚在一起）       
        #相邻两条数据的组合为： xxx1_A,xxx1_B; xxx1_A,xxx2_A; xxx1_B,xxx2_B; xxx1_A,xxx2_A
        if tag == "A":
            tag_a_host = host
            tag_a_value = values
        elif tag == "B":
            #相邻两条url的host不同，且是在B中，则输出这个url
            if tag_a_host == None or tag_a_host != host:
                value_flds = value.split("\t")
                furl = value_flds[0]
                objurl = value_flds[1]
                print "\t".join((furl, objurl))
