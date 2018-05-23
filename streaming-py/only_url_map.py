#!/bin/python
# coding=utf-8
import sys
import json
import random
import os

#map_input_file: hadoop任务的环境变量，能获得当前map脚本处理的文件名称（也就是输入的文件名称）
src_file = os.environ['map_input_file']
cnt = 0
for line in sys.stdin:
    if line != '\n':
        line = line.strip()
        # 直接将url输出，不做其他的处理，类似于hadoop的wordcount实例
        # 不同文件的格式不同，所以这里加了判断
        if 'test_path1' in src_file:
            # 按照path1的格式进行处理
            print '%s\t%s' % (furl, objurl)
        if 'test_path2' in src_file:
            # 按照path2的格式进行处理
            print '%s\t%s' % (furl, objurl)
