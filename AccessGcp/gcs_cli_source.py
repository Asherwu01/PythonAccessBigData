#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time  : 2021/5/12 11:09
# @Author: Asher Wu
# @File  : gcs_cli.py
""" pip install --upgrade google-cloud-storage """

from google.cloud import storage
import datetime

# cred = "D:\\Works\\Triwin\\Project\\GCP\\triwin-gcp-313003-83a0c2240aac.json"

"""Deletes a blob from the bucket."""

"""删除 blob """
# get storage client
# storage_client = storage.Client.from_service_account_json(cred)
storage_client = storage.Client()
buckets = storage_client.list_buckets()

for b in buckets:
    print(b.name)

""" ====== source ======"""
bucket = storage_client.bucket('gcs-source-triwin-com')

"""source:  af_install_data_history"""
# begin = datetime.date(2019, 6, 1)
# end = datetime.date(2021, 5, 18)
# for i in range((end - begin).days + 1):
#     day = begin + datetime.timedelta(days=i)
#     blob_name = "af_install_data_history/install_date=" + str(day) + "_$folder$"
#     print(blob_name)
#     blob = bucket.blob(blob_name)
#     flag = blob.exists()
#     if flag is True:
#         blob.delete()
#         print("Blob {} deleted.".format(blob_name))
#     else:
#         print("不存在")
#
# """source:  register"""
# begin = datetime.date(2018, 5, 27)
# end = datetime.date(2021, 5, 18)
# for i in range((end - begin).days + 1):
#     day = begin + datetime.timedelta(days=i)
#     blob_name = "reigister/register_date=" + str(day) + "_$folder$"
#     print(blob_name)
#     blob = bucket.blob(blob_name)
#     flag = blob.exists()
#     if flag is True:
#         blob.delete()
#         print("Blob {} deleted.".format(blob_name))
#     else:
#         print("不存在")
#
# """source:  login"""
# begin = datetime.date(2019, 9, 1)
# end = datetime.date(2021, 5, 18)
# for i in range((end - begin).days + 1):
#     day = begin + datetime.timedelta(days=i)
#     blob_name = "login/login_date=" + str(day) + "_$folder$"
#     print(blob_name)
#     blob = bucket.blob(blob_name)
#     flag = blob.exists()
#     if flag is True:
#         blob.delete()
#         print("Blob {} deleted.".format(blob_name))
#     else:
#         print("不存在")
#
# """source:  adview"""
# begin = datetime.date(2019, 9, 18)
# end = datetime.date(2021, 5, 18)
# for i in range((end - begin).days + 1):
#     day = begin + datetime.timedelta(days=i)
#     blob_name = "adview/adview_date=" + str(day) + "_$folder$"
#     print(blob_name)
#     blob = bucket.blob(blob_name)
#     flag = blob.exists()
#     if flag is True:
#         blob.delete()
#         print("Blob {} deleted.".format(blob_name))
#     else:
#         print("不存在")
#
# """source:  recharge"""
# begin = datetime.date(2018, 2, 9)
# end = datetime.date(2021, 5, 18)
# for i in range((end - begin).days + 1):
#     day = begin + datetime.timedelta(days=i)
#     blob_name = "recharge/recharge_date=" + str(day) + "_$folder$"
#     print(blob_name)
#     blob = bucket.blob(blob_name)
#     flag = blob.exists()
#     if flag is True:
#         blob.delete()
#         print("Blob {} deleted.".format(blob_name))
#     else:
#         print("不存在")
#
# """source:  spin"""
# begin = datetime.date(2019, 9, 18)
# end = datetime.date(2021, 5, 19)
# for i in range((end - begin).days + 1):
#     day = begin + datetime.timedelta(days=i)
#     blob_name = "spin/spin_date=" + str(day) + "_$folder$"
#     print(blob_name)
#     blob = bucket.blob(blob_name)
#     flag = blob.exists()
#     if flag is True:
#         blob.delete()
#         print("Blob {} deleted.".format(blob_name))
#     else:
#         print("不存在")
#
# """source:   app_spin_query/"""
#
# """source: common_event """
# begin = datetime.date(2020, 6, 22)
# end = datetime.date(2021, 5, 18)
# for i in range((end - begin).days + 1):
#     day = begin + datetime.timedelta(days=i)
#     blob_name = "common_event/event_date=" + str(day) + "_$folder$"
#     print(blob_name)
#     blob = bucket.blob(blob_name)
#     flag = blob.exists()
#     if flag is True:
#         blob.delete()
#         print("Blob {} deleted.".format(blob_name))
#     else:
#         print("不存在")
#
# """source:  app_adcost_history """
# begin = datetime.date(2020, 8, 1)
# end = datetime.date(2021, 5, 17)
# for i in range((end - begin).days + 1):
#     day = begin + datetime.timedelta(days=i)
#     blob_name = "app_adcost_history/install_date=" + str(day) + "_$folder$"
#     print(blob_name)
#     blob = bucket.blob(blob_name)
#     flag = blob.exists()
#     if flag is True:
#         blob.delete()
#         print("Blob {} deleted.".format(blob_name))
#     else:
#         print("不存在")
#
# """source:  app_level_up_history """
# begin = datetime.date(2020, 6, 22)
# end = datetime.date(2021, 5, 17)
# for i in range((end - begin).days + 1):
#     day = begin + datetime.timedelta(days=i)
#     blob_name = "app_level_up_history/level_up_date=" + str(day) + "_$folder$"
#     print(blob_name)
#     blob = bucket.blob(blob_name)
#     flag = blob.exists()
#     if flag is True:
#         blob.delete()
#         print("Blob {} deleted.".format(blob_name))
#     else:
#         print("不存在")

"""source:  user_event_history """
begin = datetime.date(2021, 5, 12)
end = datetime.date(2021, 5, 18)
for i in range((end - begin).days + 1):
    day = begin + datetime.timedelta(days=i)
    blob_name = "user_event_history/event_date=" + str(day) + "_$folder$"
    blob_name_outer = "user_event_history/event_date=" + str(day)
    print(blob_name)
    print("blob_name_outer: "+blob_name_outer)
    blob = bucket.blob(blob_name)
    flag = blob.exists()
    if flag is True:
        blob.delete()
        print("Blob {} deleted.".format(blob_name))
    else:
        print("不存在")
    """删除appid_folder"""
    for j in range(1, 62):
        blob_name_inner = blob_name_outer + "/appid=" + str(j) + "_$folder$"
        print("appid: "+blob_name_inner)
        print(blob_name_inner)
        blob = bucket.blob(blob_name_inner)
        flag = blob.exists()
        if flag is True:
            blob.delete()
            print("Blob {} deleted.".format(blob_name))
        else:
            print("不存在")
