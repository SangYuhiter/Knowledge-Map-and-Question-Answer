# -*- coding: utf-8 -*-
'''
@File  : GetDictionaryData.py
@Author: SangYu
@Date  : 2019/2/25 23:39
@Desc  : 从数据库、网络资源中获取词典信息
'''
from InformationGet import MysqlOperation
import re
import sys
from Log.Logger import MyLog

# hanlp 词典位置
dictionary_path = "../venv/Lib/site-packages/pyhanlp/static/data/dictionary/graduation"


# 学校词典（全称和简称）
def get_school_word():
    mylogger = MyLog(logger=sys._getframe().f_code.co_name).getlog()
    mylogger.info("构造学校名称词典...")
    c9 = ["北京大学", "清华大学", "复旦大学", "上海交通大学", "浙江大学",
          "南京大学", "中国科学技术大学", "哈尔滨工业大学", "西安交通大学",
          "北京大学医学部", "上海交通大学医学部", "复旦大学上海医学部"]
    c9_j = ["北大", "清华", "复旦", "上交", "浙大",
            "南大", "中科大", "哈工大", "西交大",
            "北大医学部", "上交医学部", "复旦医学部"]
    with open(dictionary_path + "/school.txt", "w", encoding="utf-8") as school_dict:
        school_dict.truncate()
        for item in c9:
            school_dict.write(item + "\n")
        for item in c9_j:
            school_dict.write(item + "\n")
    mylogger.info("构造学校名称词典完成！")


# 专业词典
def get_major_word():
    # 招生计划中的专业名称
    db_name = "university_admission"
    mydb = MysqlOperation.connect_mysql_with_db(db_name)
    mycursor = mydb.cursor()
    sql_string = "SELECT major FROM admission_plan;"
    mycursor.execute(sql_string)
    myresult = mycursor.fetchall()
    major_set1 = set()
    # for item in myresult:
    #     temp = re.findall(r"(.*)[\（\(]", item[0])
    #     if len(temp) == 0:
    #         major_set1.add(item[0])
    #     else:
    #         major_set1.add(temp[0])
    for item in myresult:
        if "(" in item[0]:
            major_set1.add(item[0].split("(")[0])
        elif "（" in item[0]:
            major_set1.add(item[0].split("（")[0])
    print("招生计划中专业名称：")
    print(len(major_set1))
    print(major_set1)

    # 录取专业中的专业名称
    db_name = "university_admission"
    mydb = MysqlOperation.connect_mysql_with_db(db_name)
    mycursor = mydb.cursor()
    sql_string = "SELECT major FROM admission_score_major;"
    mycursor.execute(sql_string)
    myresult = mycursor.fetchall()
    major_set2 = set()

    for item in myresult:
        if "(" in item[0]:
            major_set2.add(item[0].split("(")[0])
        elif "（" in item[0]:
            major_set2.add(item[0].split("（")[0])
    print("录取专业中专业名称：")
    print(len(major_set2))
    print(major_set2)

    print("以上两者的交集为")
    major_set3 = major_set1.intersection(major_set2)
    print(len(major_set3))
    print(major_set3)

    print("以上两者的并集为")
    major_set4 = major_set1.union(major_set2)
    print(len(major_set4))
    print(major_set4)

    # 根据资料构建词典
    with open(dictionary_path + "/major.txt", "w", encoding="utf-8") as major_dict:
        major_dict.truncate()
        for item in major_set4:
            major_dict.write(item + "\n")


# 百度百科获取大学专业目录
def get_university_major():
    source_path = "Information/大学/大学学科(百度百科网页源码).txt"
    with open(source_path, "r", encoding="utf-8") as source_file:
        main_page_source = source_file.read()
    # main_page_soup = BeautifulSoup(main_page_source, "lxml")
    # main_page_soup.prettify()
    #
    # source_major_list = main_page_soup.find_all("div", class_="para")
    # i=0
    # while source_major_list[i].text.find("01学科门类") == -1:
    #     i += 1
    # else:
    #     cut_index = i
    # source_major_list = source_major_list[cut_index:]
    # for item in source_major_list:
    #     print(item.text)

    # 正则方式获取大学专业目录
    result = re.findall(r'\d{4,6}[KT]*\s*[\u4e00-\u9fa5]+', main_page_source)
    # 切分部分不符合的数据
    result = result[4:-4]
    # 根据资料构建词典
    with open(dictionary_path + "/major.txt", "w", encoding="utf-8") as major_dict:
        major_dict.truncate()
        for item in result:
            major_dict.write(re.findall(r'[\u4e00-\u9fa5]+', item)[0] + "\n")


if __name__ == '__main__':
    mylogger = MyLog(logger=__name__).getlog()
    mylogger.info("start...")
    get_school_word()
    # get_major_word()
    # get_university_major()
    mylogger.info("end...")
