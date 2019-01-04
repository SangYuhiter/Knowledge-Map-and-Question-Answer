#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File  : MysqlOperation.py
@Author: SangYu
@Date  : 2018/12/21 11:22
@Desc  : Mysql连接、数据表创建、增删查改
'''

import mysql.connector


# 数据库连接（事先不确定数据库）
def connect_mysql_without_db():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="123456",
    )
    return mydb


# 数据库连接
def connect_mysql_with_db(db_name):
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="123456",
        database=db_name
    )
    return mydb


# 创建数据库university_admission
def create_database(db_name):
    mydb = connect_mysql_without_db()
    mycursor = mydb.cursor()
    mycursor.execute("SHOW DATABASES")
    dbs = []
    for db in mycursor:
        dbs.append(db[0])
        print(db[0])
    if db_name in dbs:
        print(db_name, "已存在")
    else:
        mycursor.execute("CREATE DATABASE " + db_name)
        print(db_name, "已创建")


# 查询数据库中表名
def search_table_in_db(db_name):
    mydb = connect_mysql_with_db(db_name)
    mycursor = mydb.cursor()
    mycursor.execute("SHOW TABLES")
    tables = []
    for table in mycursor:
        tables.append(table[0])
        # print(table[0])
    return tables


# 创建招生计划表
def create_admission_plan_table():
    db_name = "university_admission"
    tables = search_table_in_db(db_name)
    if "admission_plan" in tables:
        print("表已存在！")
        return
    mydb = connect_mysql_with_db(db_name)
    mycursor = mydb.cursor()
    mycursor.execute("CREATE TABLE admission_plan("
                     "id INT AUTO_INCREMENT PRIMARY KEY NOT NULL ,"
                     "school VARCHAR(30),"
                     "district VARCHAR(10),"
                     "year INT,"
                     "major VARCHAR(50),"
                     "classy varchar(10),"
                     "numbers INT)")


# 创建录取分数表
def create_admission_score_table():
    db_name = "university_admission"
    mydb = connect_mysql_with_db(db_name)
    mycursor = mydb.cursor()
    # 各省的高校分数线(学校、地区、年份、类别、批次、分数线)
    mycursor.execute("CREATE TABLE admission_score_pro("
                     "id INT AUTO_INCREMENT PRIMARY KEY NOT NULL,"
                     "school VARCHAR(30),"
                     "district VARCHAR(10),"
                     "year INT,"
                     "classy varchar(10),"
                     "batch varchar(30),"
                     "line INT)")
    # 高校的专业分数线(学校、地区、年份、类别、批次、最低分、最高分、平均分)
    mycursor.execute("CREATE TABLE admission_score_major("
                     "id INT AUTO_INCREMENT PRIMARY KEY NOT NULL,"
                     "school VARCHAR(30),"
                     "district VARCHAR(10),"
                     "year INT,"
                     "major VARCHAR(30),"
                     "classy varchar(10),"
                     "lowest INT,"
                     "highest INT,"
                     "average INT,"
                     "amount INT)")


if __name__ == "__main__":
    print("开始执行")
    db_name = "university_admission"
    # create_database(db_name)
    # search_table_in_db(db_name)
    create_admission_plan_table()
