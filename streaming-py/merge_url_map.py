#!/bin/python
# coding=utf-8
import sys
import json
import random
import os

reduce_num = 5000
#map_input_file: hadoop任务的环境变量，能获得当前map脚本处理的文件名称（也就是输入的文件名称）
src_file = os.environ['map_input_file']
cnt = 0
for line in sys.stdin:
    if line != '\n':
        line = line.strip()
        # 直接将url输出，不做其他的处理，类似于hadoop的wordcount实例
        # 首先处理B中的url
        if 'test_path1' in src_file:
            #计算出一个数字，来代表url，例如是sign
            reduce_index = sign % reduce_num
            #提取出host，用作reduce阶段的标识
            host = line.split("\t")[0]
            print '%u %s\t%s' % (reduce_index, host + "_B", url)
        # 处理A中的url
        if 'test_path2' in src_file:
            # 按照path2的格式进行处理
            #计算出一个数字，来代表url，例如是sign
            reduce_index = sign % reduce_num
            #提取出host，用作reduce阶段的标识
            host = line.split("\t")[0]
            print '%u %s\t%s' % (reduce_index, host + "_A", url)
