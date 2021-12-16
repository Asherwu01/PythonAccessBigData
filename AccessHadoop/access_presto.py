#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time  : 2021/5/6 18:26
# @Author: Asher Wu
# @File  : access_presto.py

import prestodb

conn = prestodb.dbapi.connect(host='ip-178-31-12-97.ec2.internal', port=8889, user='root', catalog='hive',
                              schema='default', http_scheme='http')
cur = conn.cursor()
conn._http_session.verify = './presto.pem'
cur.execute("select * from triwin_source.app_recharge_history where recharge_date = '2021-04-22' limit 3")
rows = cur.fetchall()
print(rows)
