#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time  : 2021/5/19 17:57
# @Author: Asher Wu
# @File  : demo.py
import numpy as np
from google.cloud import storage
import datetime

list = np.arange(1,100,10)



"""
2019-09-02~2019-09-08
2019-09-09~2019-09-15
2019-09-16~2019-09-22

2021-05-03~2021-05-09
2021-05-10~2021-05-16
"""


def bucket_info(self, bucket_name):
    bucket = self.client.bucket(bucket_name, user_project="eventdatatest")
    blobs = self.client.list_blobs(bucket)
    self.client.batch()
    for blob in blobs:
        if blob.name.__contains__("$folder$"): blob.delete()



begin = datetime.date(2019, 9, 2)
end = datetime.date(2021, 5, 18)
for dt in range((end - begin).days + 1):
    day1 = begin + datetime.timedelta(days=dt)
    day2 = begin + datetime.timedelta(days=+6)

    print(day1)
    print(day2)
    result = day1 + str(day2)
    print(day1+"~"+day2)