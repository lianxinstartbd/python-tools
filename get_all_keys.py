#!/bin/env python
# -*- coding: utf-8 -*-
import collections

def get_all_keys():
	"""
	获取map需要的key集合
	Args:
	ignore: 数据表列忽略list，在此列表中的列没有”全部“概念，只处理原值.
	Returns:
	    key集合,分隔符由KEY_DELIMITER指定.
	    示例（KEY_DELIMITER='\t'）：
	    [
		'all\tall\tall\tall\tall\tG023\tall\t10003'
		'wise\tbdbox\t3\tgeneral\tgeneral\tG009\tall\t10003'
	    ]
	"""
	#self.FIELDS: 一共有多少个key
	self.exponent = len(self.FIELDS)
	self.seed = pow(2, self.exponent)
	self.row = collections.OrderedDict()

	if not self.row:
	    raise ValueError('schema row is empty')
	row = self.row.items()
	keys = []
	# 对所有组合进行处理
	for i in range(self.seed):
	    # 获取当前组合的二进制序列，例如共有5个字段，当前组合值为4
	    # binary的值为4的二进制：100，再在前面补全两个0
	    # 最后为：00100，每一位对应一个字段
	    binary = bin(i).replace('0b', '').zfill(self.exponent)
	    ignore_flag = False
	    # 临时存储当前row当前seed生成的key
	    tmp_key = collections.OrderedDict()
	    # 对于每一个字段，如果对应值为0，表示取原值，如果为1，取all值（表示全部）
	    # 如果当前处理字段为ignore字段，那么只取原值，忽略all的情况，即此字段没有“全部”的概念
	    for j in range(self.exponent):
		if binary[j] == '0':
		    tmp_key[j] = row[j][1]
		else:
		    tmp_key[j] = 'all'
		    #position字段是int类型,使用'-1'表示全部
		    if row[j][0] == 'position':
			tmp_key[j] = '-1'
		    if row[j][0] in ignore:
			ignore_flag = True
			break
	    if ignore_flag:
		continue
	    # 处理list值情况，目前只支持row中只有一个字段是list
	    # 以show_info.show_results.card_id为例：
	    # 假定当前行数据为{1: 'bdbox', 2: ['G001', 'G002'], 3: 'ios'}
	    # 其中第一列为ua，第二列为card_id，第三列为ios
	    # 那么会生成key列表如下：
	    # [['bdbox', 'G001', 'ios'], ['bdbox', 'G002', 'ios']]
	    multi_keys = []
	    for k, v in tmp_key.iteritems():
		if isinstance(v, list):
		    for subv in v:
			tmp = tmp_key
			tmp[k] = subv
			multi_keys.append(tmp.values())
	    if multi_keys:
		keys = keys + multi_keys
	    else:
		keys.append(tmp_key.values())
	for i, key in enumerate(keys):
	    keys[i] = KEY_DELIMITER.join(key)
	# keys列表去重，解决字段原值为all的可能
	keys = reduce(lambda x, y: x if y in x else x + [y], [[], ] + keys)
	return keys


