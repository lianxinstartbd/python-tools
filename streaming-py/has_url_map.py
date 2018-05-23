#!/bin/python
# coding=utf-8
import sys

url_dict = {}
url_file = open("url_tmp.txt")
for line in url_file:
    if line == '\n':
        continue
    url = line.strip()
    if url not in url_dict:
        url_dict[url] = 1

url_file.close()

for line in sys.stdin:
    if line == '\n':
        continue
    url = line.strip().split('\t', 1)[0]
    if url in url_dict:
        print url
