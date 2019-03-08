#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File  : MysqlOperation.py
@Author: SangYu
@Date  : 2018/12/21 11:22
@Desc  : Mysql连接、数据表创建、增删查改
'''

import mysql.connector
import sys
import logging


# 日志格式设置
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
DATE_FORMAT = "%m/%d/%Y %H:%M:%S %p"
logging.basicConfig(level=logging.DEBUG, format=LOG_FORMAT, datefmt=DATE_FORMAT)


# 数据库连接（事先不确定数据库）
def connect_mysql_without_db():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="123456",
    )
    return mydb


# 数据库连接(已知数据库名)
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
    logger = logging.getLogger(sys._getframe().f_code.co_name)
    mydb = connect_mysql_without_db()
    mycursor = mydb.cursor()
    mycursor.execute("SHOW DATABASES")
    dbs = []
    logger.debug("数据库如下：")
    for db in mycursor:
        dbs.append(db[0])
        logger.debug(db[0])
    if db_name in dbs:
        logger.info("数据库"+db_name+"已存在!")
    else:
        mycursor.execute("CREATE DATABASE " + db_name)
        logger.info(db_name+"已创建!")


# 查询数据库中表名
def search_table_in_db(db_name):
    mydb = connect_mysql_with_db(db_name)
    mycursor = mydb.cursor()
    mycursor.execute("SHOW TABLES")
    tables = []
    logger.debug(db_name+"数据库中有以下表：")
    for table in mycursor:
        tables.append(table[0])
        logger.debug(table[0])
    return tables


# 创建招生计划表
def create_admission_plan_table():
    db_name = "university_admission"
    tables = search_table_in_db(db_name)
    mydb = connect_mysql_with_db(db_name)
    mycursor = mydb.cursor()

    if "admission_plan" in tables:
        logger.info("admission_plan表已存在！")
        logger.info("正在删除admission_plan表...")
        mycursor.execute("DROP TABLE admission_plan;")

    mycursor.execute("CREATE TABLE admission_plan("
                     "id INT AUTO_INCREMENT PRIMARY KEY NOT NULL ,"
                     "school VARCHAR(30),"
                     "district VARCHAR(10),"
                     "year INT,"
                     "major VARCHAR(100),"
                     "classy varchar(10),"
                     "numbers varchar(10))")
    logger.info("admission_plan表已重新创建！")


# 创建录取分数表（各省）
def create_admission_score_pro_table():
    db_name = "university_admission"
    tables = search_table_in_db(db_name)
    mydb = connect_mysql_with_db(db_name)
    mycursor = mydb.cursor()
    if "admission_score_pro" in tables:
        logger.info("admission_score_pro表已存在！")
        logger.info("正在删除admission_score_pro表...")
        mycursor.execute("DROP TABLE admission_score_pro;")
    mydb = connect_mysql_with_db(db_name)
    mycursor = mydb.cursor()
    # 各省的高校分数线(学校、地区、年份、类别、批次、分数线)
    mycursor.execute("CREATE TABLE admission_score_pro("
                     "id INT AUTO_INCREMENT PRIMARY KEY NOT NULL,"
                     "school VARCHAR(30),"
                     "year INT,"
                     "district VARCHAR(10),"
                     "batch varchar(30),"
                     "classy varchar(10),"
                     "line varchar(30))")
    logger.info("admission_score_pro表创建完成！")


# 创建录取分数表（各专业）
def create_admission_score_major_table():
    db_name = "university_admission"
    tables = search_table_in_db(db_name)
    mydb = connect_mysql_with_db(db_name)
    mycursor = mydb.cursor()
    if "admission_score_major" in tables:
        logger.info("admission_score_major表已存在！")
        logger.info("正在删除admission_score_major表...")
        mycursor.execute("DROP TABLE admission_score_major;")

    # 高校的专业分数线(学校、地区、年份、专业、类别、最高分、平均分、最低分、录取人数)
    mycursor.execute("CREATE TABLE admission_score_major("
                     "id INT AUTO_INCREMENT PRIMARY KEY NOT NULL,"
                     "school VARCHAR(30),"
                     "district VARCHAR(10),"
                     "year INT,"
                     "major VARCHAR(100),"
                     "classy varchar(30),"
                     "highest varchar(10) NULL,"
                     "average varchar(10) NULL,"
                     "lowest varchar(10),"
                     "amount varchar(10) NULL)")
    logger.info("admission_score_major表创建完成！")


# mysql 查询语句,返回查询结果
def mysql_query_sentence(mysql_string):
    dbname = "university_admission"
    mydb = connect_mysql_with_db(dbname)
    mycursor = mydb.cursor()
    mycursor.execute(mysql_string)
    myresult = mycursor.fetchall()
    return myresult

if __name__ == "__main__":
    logger = logging.getLogger(__name__)
    logger.info("begin...")
    db_name = "university_admission"
    # create_database(db_name)
    # search_table_in_db(db_name)
    create_admission_plan_table()
    create_admission_score_pro_table()
    create_admission_score_major_table()
    logger.info("end...")
