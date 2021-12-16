#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time  : 2021/5/14 10:40
# @Author: Asher Wu
# @File  : pub_sub_cli.py
from google.cloud import storage
import datetime

storage_client = storage.Client()

bucket = storage_client.bucket('gcs-sma-triwin-com')
"""sma: app_spin_query/"""
begin = 1
end = 63
for id in range(begin ,end):
    blob_name = "app_spin_query/appid=" + str(id) + "_$folder$"
    blob_name_outer = "app_spin_query/appid=" + str(id)
    print(blob_name)
    blob = bucket.blob(blob_name)
    flag = blob.exists()
    if flag is True:
        blob.delete()
        print("Blob {} deleted.".format(blob_name))
    else:
        print("不存在")
    """二级分区"""
    begin = datetime.date(2019, 11, 2)
    end = datetime.date(2021, 5, 18)
    for dt in range((end - begin).days + 1):
        day = begin + datetime.timedelta(days=dt)
        blob_name_inner = blob_name_outer+"/spin_date=" + str(day) + "_$folder$"
        print(blob_name_inner)
        blob = bucket.blob(blob_name_inner)
        flag = blob.exists()
        if flag is True:
            blob.delete()
            print("Blob {} deleted.".format(blob_name))
        else:
            print("不存在")

