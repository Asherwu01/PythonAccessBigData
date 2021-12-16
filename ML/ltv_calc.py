import pymysql
import numpy as np
from scipy.optimize import leastsq
import sys
import os
import getopt
import datetime
from configparser import ConfigParser
import json
import math


class DB():
    def __init__(self, host='localhost', port=3306, db='', username='', passowrd='', charset='utf8'):
        self.conn = pymysql.connect(host=host, port=port, db=db, user=username, passwd=passowrd, charset=charset)
        self.cur = self.conn.cursor(cursor=pymysql.cursors.DictCursor)

    def __enter__(self):
        return self.cur

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.commit()
        self.cur.close()
        self.conn.close()


def func(x, p):
    A, B = p
    return A * x ** B


def residuals(p, y, x):
    ret = y - func(x, p)
    return ret


def get_arpu(db, app_id, ltv_type, begin_date, group_type, country_list):
    if ltv_type == 'purchase':
        if group_type == 'country':
            arpuSql = "SELECT DATE_FORMAT(date,'%Y-%m-%d') AS `date`,groupType,groupName,purchaseArpu AS arpu,avgPurchaseArpuD7 AS avgArpu FROM t_ltv_arpu_data WHERE appid = {} AND groupType = '{}' AND `date` >= '{}' AND groupName IN {}" \
                .format(app_id, group_type, begin_date, country_list)
        else:
            arpuSql = "SELECT DATE_FORMAT(date,'%Y-%m-%d') AS `date`,groupType,groupName,purchaseArpu AS arpu,avgPurchaseArpuD7 AS avgArpu FROM t_ltv_arpu_data WHERE appid = {} AND groupType = '{}' AND `date` >= '{}'" \
                .format(app_id, group_type, begin_date)
    elif ltv_type == 'adview':
        if group_type == 'country':
            arpuSql = "SELECT DATE_FORMAT(date,'%Y-%m-%d') AS `date`,groupType,groupName,adviewArpu AS arpu,avgAdviewArpuD7 AS avgArpu FROM t_ltv_arpu_data WHERE appid = {} AND groupType = '{}' AND `date` >= '{}' AND groupName IN {}" \
                .format(app_id, group_type, begin_date, country_list)
        else:
            arpuSql = "SELECT DATE_FORMAT(date,'%Y-%m-%d') AS `date`,groupType,groupName,adviewArpu AS arpu,avgAdviewArpuD7 AS avgArpu FROM t_ltv_arpu_data WHERE appid = {} AND groupType = '{}' AND `date` >= '{}'" \
                .format(app_id, group_type, begin_date)
    else:
        if group_type == 'country':
            arpuSql = "SELECT DATE_FORMAT(date,'%Y-%m-%d') AS `date`,groupType,groupName,purchaseArpu + adviewArpu AS arpu,avgPurchaseArpuD7 + avgAdviewArpuD7 AS avgArpu FROM t_ltv_arpu_data WHERE appid = {} AND groupType = '{}' AND `date` >= '{}' AND groupName IN {}" \
                .format(app_id, group_type, begin_date, country_list)
        else:
            arpuSql = "SELECT DATE_FORMAT(date,'%Y-%m-%d') AS `date`,groupType,groupName,purchaseArpu + adviewArpu AS arpu,avgPurchaseArpuD7 + avgAdviewArpuD7 AS avgArpu FROM t_ltv_arpu_data WHERE appid = {} AND groupType = '{}' AND `date` >= '{}'" \
                .format(app_id, group_type, begin_date)

    diffDays = (datetime.datetime.now() - datetime.datetime.strptime(begin_date, '%Y-%m-%d')).days
    dateList = []
    for i in range(0, diffDays):
        dateList.append(
            (datetime.datetime.strptime(begin_date, '%Y-%m-%d') + datetime.timedelta(days=i)).strftime('%Y-%m-%d'))

    db.execute(arpuSql)
    arpuDic = {}
    for record in db:
        if record['groupName'] in arpuDic.keys():
            arpuDic[record['groupName']][record['date']] = record['arpu']
        else:
            arpuDic[record['groupName']] = {}
            arpuDic[record['groupName']][record['date']] = record['arpu']

    for groupName in arpuDic.keys():
        currentDateList = list(arpuDic[groupName].keys())
        missingDateList = list(set(dateList).difference(set(currentDateList)))
        missingDateList.sort()
        for addDate in missingDateList:
            arpuDic[groupName][addDate] = 0.00
    return arpuDic


def get_purchase_ltv(db, app_id, begin_date, end_date, group_type, country_list):
    if group_type == 'country':
        retention_sql = "SELECT DATE_FORMAT(date,'%Y-%m-%d') AS `date`, groupName, dnu, retainedDays, retentionRate, totalPurchaseLTV AS ltv " \
                        "FROM t_ltv_retention_data_{} " \
                        "WHERE dnu > 50 " \
                        "AND `date` >= '{}' " \
                        "AND `date` <= '{}' " \
                        "AND groupType = '{}' " \
                        "AND groupName IN {}" \
            .format(app_id, begin_date, end_date, group_type, country_list)
        self_arpu_sql = "SELECT DATE_FORMAT(date,'%Y-%m-%d') AS `date`,groupName,avg(purchaseArpu) AS avgArpu " \
                        "FROM t_ltv_retention_data_{} AS t " \
                        "WHERE `date` >= '{}'" \
                        "AND `date` <= '{}'" \
                        "AND groupType= '{}' " \
                        "AND groupName IN {} " \
                        "AND DATE_ADD(`date`, INTERVAL retainedDays DAY) >= FROM_UNIXTIME(UNIX_TIMESTAMP() - 86400 * 7, '%Y-%m-%d') " \
                        "GROUP BY t.date,groupName;" \
            .format(app_id, begin_date, end_date, group_type, country_list)
        total_arpu_sql = "SELECT groupName,avg(purchaseArpu) AS avgArpu " \
                         "FROM t_ltv_arpu_data " \
                         "WHERE appid = {} " \
                         "AND groupType= '{}' " \
                         "AND groupName IN {} " \
                         "AND `date` >= FROM_UNIXTIME(UNIX_TIMESTAMP() - 86400 * 7, '%Y-%m-%d') " \
                         "GROUP BY groupName;" \
            .format(app_id, group_type, country_list)
    else:
        retention_sql = "SELECT DATE_FORMAT(date,'%Y-%m-%d') AS `date`, groupName, dnu, retainedDays, retentionRate, totalPurchaseLTV AS ltv " \
                        "FROM t_ltv_retention_data_{} " \
                        "WHERE `date` >= '{}' " \
                        "AND `date` <= '{}' " \
                        "AND groupType = '{}'" \
            .format(app_id, begin_date, end_date, group_type)
        self_arpu_sql = "SELECT DATE_FORMAT(date,'%Y-%m-%d') AS `date`,groupName,avg(purchaseArpu) AS avgArpu " \
                        "FROM t_ltv_retention_data_{} AS t " \
                        "WHERE `date` >= '{}'" \
                        "AND `date` <= '{}'" \
                        "AND groupType= '{}' " \
                        "AND DATE_ADD(`date`, INTERVAL retainedDays DAY) >= FROM_UNIXTIME(UNIX_TIMESTAMP() - 86400 * 7, '%Y-%m-%d') " \
                        "GROUP BY t.date,groupName;" \
            .format(app_id, begin_date, end_date, group_type)
        total_arpu_sql = "SELECT groupName,avg(purchaseArpu) AS avgArpu " \
                         "FROM t_ltv_arpu_data " \
                         "WHERE appid = {} " \
                         "AND groupType= '{}' " \
                         "AND `date` >= FROM_UNIXTIME(UNIX_TIMESTAMP() - 86400 * 7, '%Y-%m-%d') " \
                         "GROUP BY groupName;" \
            .format(app_id, group_type)
    db.execute(total_arpu_sql)
    total_avg_arpu_dic = {}
    for record in db:
        total_avg_arpu_dic[record['groupName']] = record['avgArpu']

    db.execute(self_arpu_sql)
    self_avg_arpu_dic = {}
    for record in db:
        if record['groupName'] not in self_avg_arpu_dic.keys():
            self_avg_arpu_dic[record['groupName']] = {}
        self_avg_arpu_dic[record['groupName']][record['date']] = record['avgArpu']

    db.execute(retention_sql)
    real_retention_dic = {}
    for record in db:
        if record['groupName'] not in real_retention_dic.keys():
            real_retention_dic[record['groupName']] = {}
        if record['date'] not in real_retention_dic[record['groupName']].keys():
            real_retention_dic[record['groupName']][record['date']] = {}
        if 'dnu' not in real_retention_dic[record['groupName']][record['date']].keys():
            real_retention_dic[record['groupName']][record['date']]['dnu'] = record['dnu']
        if 'retentionRate' not in real_retention_dic[record['groupName']][record['date']].keys():
            real_retention_dic[record['groupName']][record['date']]['retentionRate'] = {}
        if 'ltv' not in real_retention_dic[record['groupName']][record['date']].keys():
            real_retention_dic[record['groupName']][record['date']]['ltv'] = {}
        real_retention_dic[record['groupName']][record['date']]['retentionRate'][record['retainedDays']] = round(
            record['retentionRate'], 4)
        real_retention_dic[record['groupName']][record['date']]['ltv'][record['retainedDays']] = round(record['ltv'], 4)

    retention_dic = {}
    for group_name in real_retention_dic.keys():
        retention_dic[group_name] = {}
        retained_users_dic = {}
        pa_total_dic = {}
        pa_per_day_dic = {}
        avg_retention_rate_dic = {}
        avg_lt_dic = {}
        per_user_ltv_dic = {}
        sum_ltv_dic = {}
        total_dun = 0
        for i in range(0, 366):
            retained_users_dic[i] = []
            pa_per_day_dic[i] = []
        for install_date in real_retention_dic[group_name].keys():
            dnu = real_retention_dic[group_name][install_date]['dnu']
            total_dun += dnu
            x0 = list(real_retention_dic[group_name][install_date]['retentionRate'].keys())
            y0 = list(real_retention_dic[group_name][install_date]['retentionRate'].values())
            ltv_x0 = list(real_retention_dic[group_name][install_date]['ltv'].keys())
            ltv_y0 = list(real_retention_dic[group_name][install_date]['ltv'].values())
            x2 = np.array(x0[1:])
            y2 = np.array(y0[1:])
            p0 = [0, 0]
            qs = leastsq(residuals, p0, args=(y2, x2), maxfev=100000)
            retention_rate = {}
            ltv_dic = {}
            for day in range(0, 366):
                if day < len(x0):
                    retention_rate[day] = y0[day]
                else:
                    retention_rate[day] = round(func(day, qs[0]), 4)

                if day < len(ltv_x0):
                    ltv_dic[day] = ltv_y0[day]
                elif day <= 14:
                    ltv_dic[day] = ltv_dic[day - 1] + retention_rate[day] * self_avg_arpu_dic[group_name][install_date]
                else:
                    ltv_dic[day] = ltv_dic[day - 1] + retention_rate[day] * min(total_avg_arpu_dic[group_name], self_avg_arpu_dic[group_name][install_date])

                if day == 0 and retention_rate[day] == 0:
                    retained_users_dic[day].append(dnu)
                else:
                    retained_users_dic[day].append(retention_rate[day] * dnu)

                pa_per_day_dic[day].append(ltv_dic[day] * dnu)
        for j in retained_users_dic.keys():
            avg_retention_rate_dic[j] = round(sum(retained_users_dic.get(j)) / sum(retained_users_dic.get(0)), 4)
            pa_total_dic[j] = sum(pa_per_day_dic[j])
            if j == 0:
                avg_lt_dic[j] = avg_retention_rate_dic[j]
            else:
                avg_lt_dic[j] = avg_lt_dic[j - 1] + avg_retention_rate_dic[j]
            per_user_ltv_dic[j] = round(pa_total_dic[j] / total_dun, 4)
            sum_ltv_dic[j] = pa_total_dic[j]
        retention_dic[group_name]['dnu'] = total_dun
        retention_dic[group_name]['retentionRate'] = avg_retention_rate_dic
        retention_dic[group_name]['LT'] = avg_lt_dic
        retention_dic[group_name]['perUserLTV'] = per_user_ltv_dic
        retention_dic[group_name]['sumLTV'] = sum_ltv_dic

    return retention_dic


def get_adview_ltv(db, app_id, begin_date, end_date, group_type, country_list):
    if group_type == 'country':
        retention_sql = "SELECT DATE_FORMAT(date,'%Y-%m-%d') AS `date`, groupName, dnu, retainedDays, retentionRate, totalAdviewLTV AS ltv " \
                        "FROM t_ltv_retention_data_{} " \
                        "WHERE dnu > 50 " \
                        "AND `date` >= '{}' " \
                        "AND `date` <= '{}' " \
                        "AND groupType = '{}' " \
                        "AND groupName IN {}" \
            .format(app_id, begin_date, end_date, group_type, country_list)
        self_arpu_sql = "SELECT DATE_FORMAT(date,'%Y-%m-%d') AS `date`,groupName,avg(adviewArpu) AS avgArpu " \
                        "FROM t_ltv_retention_data_{} AS t " \
                        "WHERE `date` >= '{}'" \
                        "AND `date` <= '{}'" \
                        "AND groupType= '{}' " \
                        "AND groupName IN {} " \
                        "AND DATE_ADD(`date`, INTERVAL retainedDays DAY) >= FROM_UNIXTIME(UNIX_TIMESTAMP() - 86400 * 7, '%Y-%m-%d') " \
                        "GROUP BY t.date,groupName;" \
            .format(app_id, begin_date, end_date, group_type, country_list)
        total_arpu_sql = "SELECT groupName,avg(adviewArpu) AS avgArpu " \
                         "FROM t_ltv_arpu_data " \
                         "WHERE appid = {} " \
                         "AND groupType= '{}' " \
                         "AND groupName IN {} " \
                         "AND `date` >= FROM_UNIXTIME(UNIX_TIMESTAMP() - 86400 * 7, '%Y-%m-%d') " \
                         "GROUP BY groupName;" \
            .format(app_id, group_type, country_list)
    else:
        retention_sql = "SELECT DATE_FORMAT(date,'%Y-%m-%d') AS `date`, groupName, dnu, retainedDays, retentionRate, totalAdviewLTV AS ltv " \
                        "FROM t_ltv_retention_data_{} " \
                        "WHERE `date` >= '{}' " \
                        "AND `date` <= '{}' " \
                        "AND groupType = '{}'" \
            .format(app_id, begin_date, end_date, group_type)
        self_arpu_sql = "SELECT DATE_FORMAT(date,'%Y-%m-%d') AS `date`,groupName,avg(adviewArpu) AS avgArpu " \
                        "FROM t_ltv_retention_data_{} AS t " \
                        "WHERE `date` >= '{}'" \
                        "AND `date` <= '{}'" \
                        "AND groupType= '{}' " \
                        "AND DATE_ADD(`date`, INTERVAL retainedDays DAY) >= FROM_UNIXTIME(UNIX_TIMESTAMP() - 86400 * 7, '%Y-%m-%d') " \
                        "GROUP BY t.date,groupName;" \
            .format(app_id, begin_date, end_date, group_type)
        total_arpu_sql = "SELECT groupName,avg(adviewArpu) AS avgArpu " \
                         "FROM t_ltv_arpu_data " \
                         "WHERE appid = {} " \
                         "AND groupType= '{}' " \
                         "AND `date` >= FROM_UNIXTIME(UNIX_TIMESTAMP() - 86400 * 7, '%Y-%m-%d') " \
                         "GROUP BY groupName;" \
            .format(app_id, group_type)
    print("self_arpu_sql ======== ", self_arpu_sql)
    db.execute(total_arpu_sql)
    total_avg_arpu_dic = {}
    for record in db:
        total_avg_arpu_dic[record['groupName']] = record['avgArpu']

    db.execute(self_arpu_sql)
    self_avg_arpu_dic = {}
    for record in db:
        if record['groupName'] not in self_avg_arpu_dic.keys():
            self_avg_arpu_dic[record['groupName']] = {}
        self_avg_arpu_dic[record['groupName']][record['date']] = record['avgArpu']
    print("self_avg_arpu_dic ========== ", self_avg_arpu_dic)
    db.execute(retention_sql)
    real_retention_dic = {}
    for record in db:
        if record['groupName'] not in real_retention_dic.keys():
            real_retention_dic[record['groupName']] = {}
        if record['date'] not in real_retention_dic[record['groupName']].keys():
            real_retention_dic[record['groupName']][record['date']] = {}
        if 'dnu' not in real_retention_dic[record['groupName']][record['date']].keys():
            real_retention_dic[record['groupName']][record['date']]['dnu'] = record['dnu']
        if 'retentionRate' not in real_retention_dic[record['groupName']][record['date']].keys():
            real_retention_dic[record['groupName']][record['date']]['retentionRate'] = {}
        if 'ltv' not in real_retention_dic[record['groupName']][record['date']].keys():
            real_retention_dic[record['groupName']][record['date']]['ltv'] = {}
        real_retention_dic[record['groupName']][record['date']]['retentionRate'][record['retainedDays']] = round(
            record['retentionRate'], 4)
        real_retention_dic[record['groupName']][record['date']]['ltv'][record['retainedDays']] = round(record['ltv'], 4)

    retention_dic = {}
    for group_name in real_retention_dic.keys():
        retention_dic[group_name] = {}
        retained_users_dic = {}
        pa_total_dic = {}
        pa_per_day_dic = {}
        avg_retention_rate_dic = {}
        avg_lt_dic = {}
        per_user_ltv_dic = {}
        sum_ltv_dic = {}
        total_dun = 0
        for i in range(0, 366):
            retained_users_dic[i] = []
            pa_per_day_dic[i] = []
        for install_date in real_retention_dic[group_name].keys():
            dnu = real_retention_dic[group_name][install_date]['dnu']
            total_dun += dnu
            x0 = list(real_retention_dic[group_name][install_date]['retentionRate'].keys())
            y0 = list(real_retention_dic[group_name][install_date]['retentionRate'].values())
            ltv_x0 = list(real_retention_dic[group_name][install_date]['ltv'].keys())
            ltv_y0 = list(real_retention_dic[group_name][install_date]['ltv'].values())
            x2 = np.array(x0[1:])
            y2 = np.array(y0[1:])
            p0 = [0, 0]
            qs = leastsq(residuals, p0, args=(y2, x2), maxfev=100000)
            retention_rate = {}
            ltv_dic = {}
            a = 0
            b = 0
            print("group_name ========== ", group_name)
            if self_avg_arpu_dic[group_name][install_date] > 0:
                b = math.log(20, 15 / 365)
                a = self_avg_arpu_dic[group_name][install_date] / (len(x0) ** b)
            for day in range(0, 366):
                if day < len(x0):
                    retention_rate[day] = y0[day]
                else:
                    retention_rate[day] = round(func(day, qs[0]), 4)

                if day < len(ltv_x0):
                    ltv_dic[day] = ltv_y0[day]
                elif day <= 14:
                    ltv_dic[day] = ltv_dic[day - 1] + retention_rate[day] * self_avg_arpu_dic[group_name][install_date]
                else:
                    ltv_dic[day] = ltv_dic[day - 1] + retention_rate[day] * (a * day ** b)

                if day == 0 and retention_rate[day] == 0:
                    retained_users_dic[day].append(dnu)
                else:
                    retained_users_dic[day].append(retention_rate[day] * dnu)

                pa_per_day_dic[day].append(ltv_dic[day] * dnu)
        for j in retained_users_dic.keys():
            avg_retention_rate_dic[j] = round(sum(retained_users_dic.get(j)) / sum(retained_users_dic.get(0)), 4)
            pa_total_dic[j] = sum(pa_per_day_dic[j])
            if j == 0:
                avg_lt_dic[j] = avg_retention_rate_dic[j]
            else:
                avg_lt_dic[j] = avg_lt_dic[j - 1] + avg_retention_rate_dic[j]
            per_user_ltv_dic[j] = round(pa_total_dic[j] / total_dun, 4)
            sum_ltv_dic[j] = pa_total_dic[j]
        retention_dic[group_name]['dnu'] = total_dun
        retention_dic[group_name]['retentionRate'] = avg_retention_rate_dic
        retention_dic[group_name]['LT'] = avg_lt_dic
        retention_dic[group_name]['perUserLTV'] = per_user_ltv_dic
        retention_dic[group_name]['sumLTV'] = sum_ltv_dic

    return retention_dic


def get_all_ltv(db, app_id, begin_date, end_date, group_type, country_list):
    purchase_retention_dic = get_purchase_ltv(db, app_id, begin_date, end_date, group_type, country_list)
    adview_retention_dic = get_adview_ltv(db, app_id, begin_date, end_date, group_type, country_list)
    total_retention_dic = purchase_retention_dic
    for group_name in adview_retention_dic.keys():
        for day in adview_retention_dic[group_name]['perUserLTV'].keys():
            total_retention_dic[group_name]['perUserLTV'][day] = purchase_retention_dic[group_name]['perUserLTV'][day] + \
                                                                 adview_retention_dic[group_name]['perUserLTV'][day]
        for day in adview_retention_dic[group_name]['sumLTV'].keys():
            total_retention_dic[group_name]['sumLTV'][day] = purchase_retention_dic[group_name]['sumLTV'][day] + \
                                                             adview_retention_dic[group_name]['sumLTV'][day]
    return total_retention_dic


def get_ltv(db, app_id, ltv_type, begin_date, end_date, group_type, country_list):
    if ltv_type == 'purchase':
        retention_dic = get_purchase_ltv(db, app_id, begin_date, end_date, group_type, country_list)
    elif ltv_type == 'adview':
        retention_dic = get_adview_ltv(db, app_id, begin_date, end_date, group_type, country_list)
    else:
        retention_dic = get_all_ltv(db, app_id, begin_date, end_date, group_type, country_list)
    return retention_dic


def main(argv):
    app_id = ''
    ltv_type = 'purchase'
    begin_date = (datetime.date.today() - datetime.timedelta(days=7)).strftime('%Y-%m-%d')
    end_date = (datetime.date.today() - datetime.timedelta(days=7)).strftime('%Y-%m-%d')
    group_type = 'mediaSource'
    # groupName = 'ALL'
    # method = "ALL"
    try:
        opts, args = getopt.getopt(argv,
                                   'ha:b:e:t:n:l:',
                                   ["help", "app_id=", "begin_date=", "end_date=", "group_type=", "groupName=",
                                    "ltv_type"])
    except getopt.GetoptError:
        print("ERROR: ltv_calc.py -a <app_id> (-b <begin_date> -e <end_date> -t <group_type> -n <groupName>)")
        print("OR: ltv_calc.py --app_id=<app_id> "
              "(--ltv_type=<ltv_type> "
              "--begin_date=<begin_date> "
              "--end_date=<end_date> "
              "--group_type=<group_type> "
              "--groupName=<groupName>)")
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print(
                'ltv_calc.py -a <app_id> (-b <begin_date> -e <end_date> -t <group_type> -n <groupName> -l <ltv_type>)')
            print('or: ltv_calc.py --app_id=<app_id> '
                  '(--ltv_type=<ltv_type> '
                  '--begin_date=<begin_date> '
                  '--end_date=<end_date> '
                  '--group_type=<group_type> '
                  '--groupName=<groupName>)')
            sys.exit(2)
        elif opt in ("-l", "--ltv_type"):
            ltv_type = arg
        elif opt in ("-a", "--app_id"):
            app_id = arg
        elif opt in ("-b", "--begin_date"):
            begin_date = arg
        elif opt in ("-e", "--end_date"):
            end_date = arg
        elif opt in ("-t", "--group_type"):
            group_type = arg
        # elif opt in ("-n", "--groupName"):
        #     groupName = arg
    if end_date < begin_date:
        ex = Exception("Please set the correct date range : end_date >= startDate")
        raise ex

    current_path = os.path.split(os.path.realpath(__file__))[0]

    config_file_path = current_path + '/config.ini'
    config = ConfigParser()
    config.read(config_file_path)
    hostname = config.get('mysql', 'hostname')
    port = int(config.get('mysql', 'port'))
    username = config.get('mysql', 'username')
    password = config.get('mysql', 'password')
    database = config.get('mysql', 'database')
    country_list = config.get('group_type', 'country')
    with DB(host=hostname, port=port, username=username, passowrd=password, db=database) as db:
        arpu_dic = get_arpu(db=db, app_id=app_id, ltv_type=ltv_type, begin_date=begin_date, group_type=group_type,
                            country_list=country_list)
        ltv_dic = get_ltv(db=db, app_id=app_id, ltv_type=ltv_type, begin_date=begin_date, end_date=end_date,
                          group_type=group_type,
                          country_list=country_list)

    resultDic = {}
    resultDic['arpu'] = arpu_dic
    resultDic['ltv'] = ltv_dic
    resultJsonStr = json.dumps(resultDic)
    print(resultJsonStr)


if __name__ == '__main__':
    main(sys.argv[1:])
