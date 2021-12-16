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

""" ====== sma ======"""
bucket = storage_client.bucket('gcs-sma-triwin-com')

"""sma:  af_install_data_history"""
begin = 1
end = 63
for id in range(begin ,end):
    blob_name = "af_install_users/appid=" + str(id) + "_$folder$"
    print(blob_name)
    blob = bucket.blob(blob_name)
    flag = blob.exists()
    if flag is True:
        blob.delete()
        print("Blob {} deleted.".format(blob_name))
    else:
        print("不存在")

"""sma:  app_active_users/"""
begin = datetime.date(2019, 9, 1)
end = datetime.date(2021, 5, 18)
for dt in range((end - begin).days + 1):
    day = begin + datetime.timedelta(days=dt)
    blob_name = "app_active_users/active_date=" + str(day) + "_$folder$"
    print(blob_name)
    blob = bucket.blob(blob_name)
    flag = blob.exists()
    if flag is True:
        blob.delete()
        print("Blob {} deleted.".format(blob_name))
    else:
        print("不存在")

"""sma:  app_common_event_attributes/"""
begin = 1
end = 63
for id in range(begin ,end):
    blob_name = "app_common_event_attributes/appid=" + str(id) + "_$folder$"
    print(blob_name)
    blob = bucket.blob(blob_name)
    flag = blob.exists()
    if flag is True:
        blob.delete()
        print("Blob {} deleted.".format(blob_name))
    else:
        print("不存在")

"""sma: app_common_event_count"""

"""sma: app_count_analysis/"""

"""sma: app_install_cnt/"""

"""sma: app_login_distinct/"""
begin = datetime.date(2019, 9, 1)
end = datetime.date(2021, 5, 18)
for dt in range((end - begin).days + 1):
    day = begin + datetime.timedelta(days=dt)
    blob_name = "app_login_distinct/login_date=" + str(day) + "_$folder$"
    print(blob_name)
    blob = bucket.blob(blob_name)
    flag = blob.exists()
    if flag is True:
        blob.delete()
        print("Blob {} deleted.".format(blob_name))
    else:
        print("不存在")

"""sma: app_purchase_item/"""

"""sma: app_recharge_analysis/"""

"""sma: app_register_month_cnt/"""

"""sma: app_register_users/"""
begin = 1
end = 63
for id in range(begin ,end):
    blob_name = "app_register_users/appid=" + str(id) + "_$folder$"
    print(blob_name)
    blob = bucket.blob(blob_name)
    flag = blob.exists()
    if flag is True:
        blob.delete()
        print("Blob {} deleted.".format(blob_name))
    else:
        print("不存在")

"""sma: app_register_week_cnt/"""

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

"""sma: filter_app_install_users/"""

"""sma: filter_app_register_users/"""

"""sma: filter_dimension/"""

"""sma: filter_firstpay_cnt/"""

"""sma: filter_firstpay_users"""

"""sma: filter_install_cnt/"""

"""sma: filter_install_cnt/"""

"""sma: filter_register_cnt/"""

"""sma: user_churn_predict_features/"""
begin = datetime.date(2020, 7, 20)
end = datetime.date(2021, 5, 18)
for dt in range((end - begin).days + 1):
    day = begin + datetime.timedelta(days=dt)
    blob_name = "app_login_distinct/login_date=" + str(day) + "_$folder$"
    print(blob_name)
    blob = bucket.blob(blob_name)
    flag = blob.exists()
    if flag is True:
        blob.delete()
        print("Blob {} deleted.".format(blob_name))
    else:
        print("不存在")

"""sma: user_last_10_recharge_spin_data"""
begin = 1
end = 63
for id in range(begin ,end):
    blob_name = "user_last_10_recharge_spin_data/appid=" + str(id) + "_$folder$"
    print(blob_name)
    blob = bucket.blob(blob_name)
    flag = blob.exists()
    if flag is True:
        blob.delete()
        print("Blob {} deleted.".format(blob_name))
    else:
        print("不存在")

"""sma: user_last_4_adview_data"""
begin = 1
end = 63
for id in range(begin ,end):
    blob_name = "user_last_4_adview_data/appid=" + str(id) + "_$folder$"
    print(blob_name)
    blob = bucket.blob(blob_name)
    flag = blob.exists()
    if flag is True:
        blob.delete()
        print("Blob {} deleted.".format(blob_name))
    else:
        print("不存在")


"""sma: user_login_balance"""
begin = 1
end = 63
for id in range(begin ,end):
    blob_name = "user_login_balance/appid=" + str(id) + "_$folder$"
    print(blob_name)
    blob = bucket.blob(blob_name)
    flag = blob.exists()
    if flag is True:
        blob.delete()
        print("Blob {} deleted.".format(blob_name))
    else:
        print("不存在")

"""sma: user_login_details"""
begin = 1
end = 63
for id in range(begin ,end):
    blob_name = "user_login_details/appid=" + str(id) + "_$folder$"
    print(blob_name)
    blob = bucket.blob(blob_name)
    flag = blob.exists()
    if flag is True:
        blob.delete()
        print("Blob {} deleted.".format(blob_name))
    else:
        print("不存在")


"""sma: user_spin_data_before_recharge/"""
begin = datetime.date(2018, 2, 9)
end = datetime.date(2021, 5, 18)
for dt in range((end - begin).days + 1):
    day = begin + datetime.timedelta(days=dt)
    blob_name = "user_spin_data_before_recharge/recharge_date=" + str(day) + "_$folder$"
    print(blob_name)
    blob = bucket.blob(blob_name)
    flag = blob.exists()
    if flag is True:
        blob.delete()
        print("Blob {} deleted.".format(blob_name))
    else:
        print("不存在")

"""sma: user_spin_details"""
begin = 1
end = 63
for id in range(begin ,end):
    blob_name = "user_spin_details/appid=" + str(id) + "_$folder$"
    print(blob_name)
    blob = bucket.blob(blob_name)
    flag = blob.exists()
    if flag is True:
        blob.delete()
        print("Blob {} deleted.".format(blob_name))
    else:
        print("不存在")
