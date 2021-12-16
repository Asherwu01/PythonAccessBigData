#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time  : 2021/12/16 8:36
# @Author: Asher Wu
# @File  : access_phoenix.py

import jaydebeapi

# 获取连接对象
conn = jaydebeapi.connect('org.apache.phoenix.jdbc.PhoenixDriver',
                          'jdbc:phoenix:ip-178-31-13-201.ec2.internal:2181',
                          {'phoenix.schema.isNamespaceMappingEnabled': 'false'},
                          'E://ProgramFiles//PyCharm//Data//PycharmProject//PHPAccessPhoenixAPI//venv//Lib//phoenix-client.jar')

# 创建cursor
curs = conn.cursor()

# 通过 cursor 执行sql
curs.execute('select * from TAG.APP_1_USER_TAGS limit 1')
cols = [t[0] for t in curs.description]

# 获取查询结果
result = curs.fetchall()

print(result)