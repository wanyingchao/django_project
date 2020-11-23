from django.db import models
import pymysql
import os, sys, time
import requests
import json


# Create your models here.


class MySql:
    def __init__(self):
        self.connection = pymysql.connect(host='rr-bp10f2937ic701lo4mo.mysql.rds.aliyuncs.com',
                                          user='root',
                                          password='JZCD400-6799869jcshbdd!',
                                          db='charge',
                                          charset='utf8',
                                          cursorclass=pymysql.cursors.DictCursor)

    def insert(self, sql, data):
        # 当表中有自增的主键的时候，可以使用lastrowid来获取最后一次自增的ID：cursor.lastrowid
        # 建立游标
        cursor = self.connection.cursor()
        # 执行sql
        cursor.execute(sql, data)
        # 提交操作，没有commit数据库不会保存
        self.connection.commit()
        # 关闭游标
        cursor.close()
        # 关闭连接
        self.connection.close()

    def select(self, sql):
        cursor = self.connection.cursor()
        cursor.execute(sql)
        # fetchone(): 获取下一行数据，第一次为首行；
        # fetchall(): 获取所有行数据源
        # fetchmany(4): 获取下4行数据
        results = cursor.fetchall()
        cursor.close()
        self.connection.close()
        return results


class PopDjango:
    def __init__(self):
        self.url = 'https://www.jzcdsc.com/charge/device/pop'
        interface_path = os.path.dirname(__file__)
        sys.path.insert(0, interface_path)   # 将当前文件的父目录加入临时系统变量

    def pop_interface(self, deviceid, slot, text):
        par = {
            'deviceid': deviceid,
            'slot': slot
        }
        body = {
            'Content-Type': 'application/json;charset=utf-8',
        }
        r = requests.post(self.url, par, body, verify=True)
        result = time.strftime('%Y-%m-%d %H:%M:%S') + ' ' + deviceid + " " + str(
            slot) + "口" + r.text
        text.append(result)

    def pop_loop(self, deviceid, text):
        if deviceid[4] + deviceid[5] == '06':
            for slot in range(1, 7):
                self.pop_interface(deviceid, slot, text)
                if slot == 6:
                    text.append(
                        '---------------------------------------------------------------------------------------')
        elif deviceid[4] + deviceid[5] == '09':
            for slot in range(1, 10):
                self.pop_interface(deviceid, slot, text)
                if slot == 9:
                    text.append(
                        '---------------------------------------------------------------------------------------')
        else:
            for slot in range(1, 13):
                self.pop_interface(deviceid, slot, text)
                if slot == 12:
                    text.append(
                        '---------------------------------------------------------------------------------------')


class SelectSignal:
    def __init__(self):
        self.url = 'https://www.jzcdsc.com:443/charge/device/signal'

    def select_signal(self, deviceid):
        par = {
            'deviceid': deviceid,
        }
        r = requests.get(self.url, par, verify=True)
        results = json.loads(r.text)
        return results

