#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File  : InsertAdmissionData.py
@Author: SangYu
@Date  : 2018/12/25 14:03
@Desc  : 此程序用于将招生数据插入数据库
'''
from InformationGet import MysqlOperation
from FileRead.FileNameRead import read_all_file_list
from Log.Logger import MyLog
import sys


# 读取文档内容
def read_file_content(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return file.readlines()


# 获取招生计划文档构造表项列表
def plan_doc_to_mysql_table_tuple(file_path, school):
    mylogger = MyLog(logger=sys._getframe().f_code.co_name).getlog()
    mylogger.info("插入文件"+file_path)
    file_content = read_file_content(file_path)
    file_name = file_path.split("\\")[-1]
    year = file_name.split("-")[0]
    district = file_name.split("-")[1]
    mylogger.debug("年份："+year+"地区："+district)
    table_content = []
    for i in range(len(file_content)):
        file_content[i] = file_content[i].strip()
        temp = file_content[i].split("\t")
        table_content.append(temp)
    table_head = table_content[0]
    mylogger.debug("表头："+str(table_head))
    table_content = table_content[1:]
    # 去除统计部分的数据项、无数据的项
    for item in table_content:
        if item[0] == "无数据":
            table_content.remove(item)
        # elif item[1] == "统计":
        #     table_content.remove(item)
    mysql_content = []
    for item in table_content:
        major = item[0]
        classy = item[1]
        numbers = item[2]
        temp = (school, district, year, major, classy, numbers)
        mysql_content.append(temp)
    mylogger.debug("构造后的数据表项如下：")
    for item in mysql_content:
        mylogger.debug(str(item))
    return mysql_content


# 插入数据库表admission_plan(一张表)
def insert_table_admission_plan(mysql_tuple_list):
    db_name = "university_admission"
    mydb = MysqlOperation.connect_mysql_with_db(db_name)
    mycursor = mydb.cursor()
    sql_string = "INSERT INTO admission_plan(school,district,year,major,classy,numbers) " \
                 "VALUES (%s,%s,%s,%s,%s,%s)"
    mycursor.executemany(sql_string, mysql_tuple_list)
    mydb.commit()


# 插入所有学校的数据
def insert_all_school_table_admission_plan():
    c9 = ["北京大学", "清华大学", "复旦大学", "上海交通大学", "浙江大学",
          "南京大学", "中国科学技术大学", "哈尔滨工业大学", "西安交通大学",
          "北京大学医学部"]
    already_get = ["西安交通大学"]
    for school in already_get:
        mylogger.info("开始插入"+school+"的招生计划数据...")
        dir_path = "Information/九校联盟/" + school + "/招生计划"
        file_list = read_all_file_list(dir_path)
        for file in file_list:
            mylogger.info("构造数据项元组...")
            mysql_content = plan_doc_to_mysql_table_tuple(file, school)
            mylogger.info("将元组数据插入数据库...")
            insert_table_admission_plan(mysql_content)
            mylogger.info("元组数据插入完成!")


# 获取录取分数（各专业）文档构造表项列表
def score_major_doc_to_mysql_table_tuple(file_path, school):
    file_content = read_file_content(file_path)
    file_name = file_path.split("\\")[-1]
    year = file_name.split("-")[0]
    district = file_name.split("-")[1]
    table_format = file_name.split("-")[-1]
    print("年份：", year, "地区：", district, "表类型：", table_format)
    table_content = []
    for i in range(len(file_content)):
        file_content[i] = file_content[i].strip().replace("-", "NULL")
        temp = file_content[i].split("\t")
        table_content.append(temp)
    table_head = table_content[0]
    print("表头：", table_head)
    table_content = table_content[1:]
    # # 去除统计部分的数据项、无数据的项
    # for item in table_content:
    #     if item[0] == "无数据":
    #         table_content.remove(item)
    #     elif item[1] == "统计":
    #         table_content.remove(item)
    mysql_content = []
    for item in table_content:
        major = item[0]
        classy = item[1]
        highest = item[2]
        average = item[3]
        lowest = item[4]
        amount = item[5]
        temp = (school, district, year, major, classy, highest, average, lowest, amount)
        mysql_content.append(temp)
    # for item in mysql_content:
    #     print(item)
    return mysql_content


# 插入数据库表admission_score_major(一张表)
def insert_table_admission_score_major(mysql_tuple_list):
    db_name = "university_admission"
    mydb = MysqlOperation.connect_mysql_with_db(db_name)
    mycursor = mydb.cursor()
    sql_string = "INSERT INTO admission_score_major(school,district,year,major,classy,highest,average,lowest,amount) " \
                 "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    mycursor.executemany(sql_string, mysql_tuple_list)
    mydb.commit()


# 获取录取分数（各省份）文档构造表项列表
def score_pro_doc_to_mysql_table_tuple(file_path, school):
    file_content = read_file_content(file_path)
    file_name = file_path.split("\\")[-1]
    year = file_name.split("-")[0]
    table_format = file_name.split("-")[-1]
    print("年份：", year, "表类型：", table_format)
    table_content = []
    for i in range(len(file_content)):
        file_content[i] = file_content[i].strip().replace("-", "NULL")
        temp = file_content[i].split("\t")
        table_content.append(temp)
    table_head = table_content[0]
    print("表头：", table_head)
    table_content = table_content[1:]
    mysql_content = []
    for item in table_content:
        district = item[0]
        batch = item[1]
        classy = item[2]
        line = item[3]
        temp = (school, year, district, batch, classy, line)
        mysql_content.append(temp)
    # for item in mysql_content:
    #     print(item)
    return mysql_content


# 插入数据库表admission_score_pro(一张表)
def insert_table_admission_score_pro(mysql_tuple_list):
    db_name = "university_admission"
    mydb = MysqlOperation.connect_mysql_with_db(db_name)
    mycursor = mydb.cursor()
    sql_string = "INSERT INTO admission_score_pro(school,year,district,batch,classy,line) " \
                 "VALUES (%s,%s,%s,%s,%s,%s)"
    mycursor.executemany(sql_string, mysql_tuple_list)
    mydb.commit()


# 插入所有学校的数据(录取分数，分专业和分省份)
def insert_all_school_table_admission_score():
    c9 = ["北京大学", "清华大学", "复旦大学", "上海交通大学", "浙江大学",
          "南京大学", "中国科学技术大学", "哈尔滨工业大学", "西安交通大学",
          "北京大学医学部","上海交通大学医学部"]
    already_get = ["浙江大学"]
    for school in already_get:
        dir_path = "Information/九校联盟/" + school + "/录取分数"
        file_list = read_all_file_list(dir_path)
        for file in file_list:
            table_format = file.split("-")[-1]
            print(table_format)
            if table_format == "major":
                mysql_content = score_major_doc_to_mysql_table_tuple(file, school)
                insert_table_admission_score_major(mysql_content)
            elif table_format == "pro":
                mysql_content = score_pro_doc_to_mysql_table_tuple(file, school)
                insert_table_admission_score_pro(mysql_content)
            for item in mysql_content:
                print(item)


if __name__ == "__main__":
    mylogger = MyLog(logger=sys._getframe().f_code.co_name).getlog()
    mylogger.info("begin...")
    mylogger.info("插入所有学校的招生计划数据...")
    # insert_all_school_table_admission_plan()
    mylogger.info("插入所有学校的录取分数数据...")
    insert_all_school_table_admission_score()
    mylogger.info("end...")
    mylogger.debug("**********")
