#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File  : MysqlOperation.py
@Author: SangYu
@Date  : 2018/12/21 11:22
@Desc  : Mysql连接、数据表创建、增删查改
'''

import mysql.connector


# 数据库连接
def connect_mysql():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="123456",
        database="university_admission"
    )
    return mydb


# 创建招生计划表
def create_admission_plan_table():
    mydb = connect_mysql()
    mycursor = mydb.cursor()
    mycursor.execute("CREATE TABLE admission_plan("
                     "id INT AUTO_INCREMENT PRIMARY KEY NOT NULL ,"
                     "school VARCHAR(30),"
                     "district VARCHAR(10),"
                     "major VARCHAR(30),"
                     "year INT,"
                     "classy varchar(10),"
                     "numbers INT)")


# 创建录取分数表
def create_admission_score_table():
    mydb = connect_mysql()
    mycursor = mydb.cursor()
    # 各省的高校分数线(学校、地区、年份、类别、批次、最低分、最高分)
    mycursor.execute("CREATE TABLE admission_score_pro("
                     "id INT AUTO_INCREMENT PRIMARY KEY NOT NULL,"
                     "school VARCHAR(30),"
                     "district VARCHAR(10),"
                     "year INT,"
                     "classy varchar(10),"
                     "batch varchar(30),"
                     "lowest INT,"
                     "highest INT,"
                     "average INT)")
    # 高校的专业分数线
    mycursor.execute("CREATE TABLE admission_score_major("
                     "id INT AUTO_INCREMENT PRIMARY KEY NOT NULL,"
                     "school VARCHAR(30),"
                     "district VARCHAR(10),"
                     "major VARCHAR(30),"
                     "year INT,"
                     "classy varchar(10),"
                     "lowest INT,"
                     "highest INT,"
                     "average INT,"
                     "amount INT)")


if __name__ == "__main__":
    print("开始执行")