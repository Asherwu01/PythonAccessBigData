#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time  : 2021/5/6 18:07
# @Author: Asher Wu
# @File  : access_hive.py
from impala.dbapi import connect

conn = connect(host='ip-178-31-12-97.ec2.internal', port=10000, auth_mechanism='PLAIN', database='triwin_source')
cur = conn.cursor()
cur.execute("select * from triwin_source.app_recharge_history where recharge_date = '2021-04-22' limit 3")
for result in cur.fetchall():
    print(result)
