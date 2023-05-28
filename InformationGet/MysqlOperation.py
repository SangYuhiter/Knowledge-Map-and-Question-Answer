# -*- coding: utf-8 -*-
"""
@File  : MysqlOperation.py
@Author: SangYu
@Date  : 2018/12/21 11:22
@Desc  : Mysql连接、数据表创建、增删查改
"""
import pymysql
import sys
from Log.Logger import MyLog


# 数据库连接（事先不确定数据库）
def connect_mysql_without_db():
    mydb = pymysql.Connect(
        host="localhost",
        user="root",
        passwd="123456",
    )
    return mydb


# 数据库连接(已知数据库名)
def connect_mysql_with_db(db_name: str)->pymysql.Connect:
    """
    数据库连接(已知数据库名)
    :param db_name: 数据库名
    :return: 数据库连接
    """
    mydb = pymysql.Connect(
        host="localhost",
        user="root",
        passwd="123456",
        database=db_name
    )
    return mydb


# 创建数据库university_admission
# noinspection PyProtectedMember
def create_database(db_name: str):
    """
    创建数据库university_admission
    :param db_name: 数据库名
    :return:
    """
    function_logger = MyLog(logger=sys._getframe().f_code.co_name).getlog()
    mydb = connect_mysql_without_db()
    mycursor = mydb.cursor()
    mycursor.execute("SHOW DATABASES")
    dbs = []
    function_logger.debug("数据库如下：")
    for db in mycursor:
        dbs.append(db[0])
        function_logger.debug(db[0])
    if db_name in dbs:
        function_logger.info("数据库" + db_name + "已存在!")
    else:
        mycursor.execute("CREATE DATABASE " + db_name)
        function_logger.info(db_name + "已创建!")


# 查询数据库中表名
# noinspection PyProtectedMember
def search_table_in_db(db_name: str)->list:
    """
    查询数据库中表名
    :param db_name: 数据库名
    :return: 数据库中表名列表
    """
    function_logger = MyLog(logger=sys._getframe().f_code.co_name).getlog()
    mydb = connect_mysql_with_db(db_name)
    mycursor = mydb.cursor()
    mycursor.execute("SHOW TABLES")
    tables = []
    function_logger.debug(db_name + "数据库中有以下表：")
    for table in mycursor:
        tables.append(table[0])
        function_logger.debug(table[0])
    return tables


# 创建招生计划表
# noinspection PyProtectedMember,SqlResolve
def create_admission_plan_table():
    function_logger = MyLog(logger=sys._getframe().f_code.co_name).getlog()
    db_name = "university_admission"
    tables = search_table_in_db(db_name)
    mydb = connect_mysql_with_db(db_name)
    mycursor = mydb.cursor()

    if "admission_plan" in tables:
        function_logger.info("admission_plan表已存在！")
        function_logger.info("正在删除admission_plan表...")
        mycursor.execute("DROP TABLE admission_plan;")

    mycursor.execute("CREATE TABLE admission_plan("
                     "id INT AUTO_INCREMENT PRIMARY KEY NOT NULL ,"
                     "school VARCHAR(30),"
                     "district VARCHAR(10),"
                     "year INT,"
                     "major VARCHAR(100),"
                     "classy varchar(10),"
                     "numbers varchar(10))")
    function_logger.info("admission_plan表已重新创建！")


# 创建录取分数表（各省）
# noinspection PyProtectedMember,SqlResolve
def create_admission_score_pro_table():
    function_logger = MyLog(logger=sys._getframe().f_code.co_name).getlog()
    db_name = "university_admission"
    tables = search_table_in_db(db_name)
    mydb = connect_mysql_with_db(db_name)
    mycursor = mydb.cursor()
    if "admission_score_pro" in tables:
        function_logger.info("admission_score_pro表已存在！")
        function_logger.info("正在删除admission_score_pro表...")
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
    function_logger.info("admission_score_pro表创建完成！")


# 创建录取分数表（各专业）
# noinspection PyProtectedMember,SqlResolve
def create_admission_score_major_table():
    function_logger = MyLog(logger=sys._getframe().f_code.co_name).getlog()
    db_name = "university_admission"
    tables = search_table_in_db(db_name)
    mydb = connect_mysql_with_db(db_name)
    mycursor = mydb.cursor()
    if "admission_score_major" in tables:
        function_logger.info("admission_score_major表已存在！")
        function_logger.info("正在删除admission_score_major表...")
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
    function_logger.info("admission_score_major表创建完成！")


# mysql 查询语句,返回查询结果
def mysql_query_sentence(mysql_string: str)->list:
    """
    mysql 查询语句,返回查询结果,记录键值列表
    :param mysql_string: MySQL查询语句
    :return: 记录键值列表
    """
    dbname = "university_admission"
    mydb = connect_mysql_with_db(dbname)
    mycursor = mydb.cursor()
    mycursor.execute(mysql_string)
    des = mycursor.description
    column_name = [column[0] for column in des]
    tempresult = mycursor.fetchall()
    myresult = []
    for record in tempresult:
        record_dict = {}
        for column, word in zip(column_name, record):
            record_dict[column] = word
        myresult.append(record_dict)
    return myresult


# 查询指定表的表头
def query_table_head(table_name: str)->list:
    """
    查询指定表的表头
    :param table_name: 表名
    :return: 表头列表
    """
    dbname = "university_admission"
    mydb = connect_mysql_with_db(dbname)
    mycursor = mydb.cursor()
    mysql_string = "select id from " + table_name + "where id ='1';"
    mycursor.execute(mysql_string)
    des = mycursor.description
    column_name = [column[0] for column in des]
    return column_name


if __name__ == "__main__":
    main_logger = MyLog(logger=__name__).getlog()
    main_logger.info("begin...")
    # db_name = "university_admission"
    # create_database(db_name)
    # search_table_in_db(db_name)
    # create_admission_plan_table()
    # create_admission_score_pro_table()
    # create_admission_score_major_table()
    # noinspection SqlResolve
    test_myresult = mysql_query_sentence("select * from admission_plan where id='1';")
    for item in test_myresult:
        print(item)
    main_logger.info("end...")
