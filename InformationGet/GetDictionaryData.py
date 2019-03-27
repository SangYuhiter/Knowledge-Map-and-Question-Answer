# -*- coding: utf-8 -*-
"""
@File  : GetDictionaryData.py
@Author: SangYu
@Date  : 2019/2/25 23:39
@Desc  : 从数据库、网络资源中获取词典信息
"""
from InformationGet.MysqlOperation import mysql_query_sentence
import re
import sys
from Log.Logger import MyLog
from pypinyin import lazy_pinyin

# hanlp 词典位置
dictionary_path = "../venv/Lib/site-packages/pyhanlp/static/data/dictionary/graduation"


# 学校词典（全称和简称）
# noinspection PyProtectedMember
def build_school_dict():
    function_logger = MyLog(logger=sys._getframe().f_code.co_name).getlog()
    function_logger.info("构造学校名称词典...")
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
    function_logger.info("构造学校名称词典完成！")


# 专业词典，从mysql表中获取，以提高问句中专业的识别率
# noinspection PyProtectedMember,SqlResolve
def build_mysql_major_dict():
    function_logger = MyLog(logger=sys._getframe().f_code.co_name).getlog()
    function_logger.info("获取招生计划表中的专业字段...")
    # 招生计划中的专业名称
    plan_sql_string = "SELECT major FROM admission_plan GROUP BY major;"
    myresult = mysql_query_sentence(plan_sql_string)
    function_logger.debug("招生计划表中专业数%d:" % len(myresult))
    pattern = re.compile(r"[(（[].*?[)）\]].*")
    plan_major_set = set()
    for major in myresult:
        temp = re.sub(pattern, "", major[0])
        plan_major_set.add(temp)
    function_logger.debug("招生计划表中专业数(统计合并后):%d" % len(plan_major_set))
    function_logger.debug(str(sorted(list(plan_major_set), key=lambda x: lazy_pinyin(x.lower())[0][0])))

    # 录取分数中的专业名称
    score_sql_string = "SELECT major FROM admission_score_major GROUP BY major;"
    myresult = mysql_query_sentence(score_sql_string)
    function_logger.debug("录取分数表中专业数%d:" % len(myresult))
    score_major_set = set()
    for major in myresult:
        temp = re.sub(pattern, "", major[0])
        score_major_set.add(temp)
    function_logger.debug("录取分数表中专业数(统计合并后):%d" % len(score_major_set))
    function_logger.debug(str(sorted(list(score_major_set), key=lambda x: lazy_pinyin(x.lower())[0][0])))

    # 测定两者交集
    function_logger.debug("以上两者的交集为：")
    major_and_set = plan_major_set.intersection(score_major_set)
    function_logger.debug("交集长度为：%d", len(major_and_set))
    function_logger.debug(str(sorted(list(major_and_set), key=lambda x: lazy_pinyin(x.lower())[0][0])))

    # 测定两者并集
    function_logger.debug("以上两者的并集为：")
    major_or_set = plan_major_set.union(score_major_set)
    function_logger.debug("并集长度为：%d", len(major_or_set))
    function_logger.debug(str(sorted(list(major_or_set), key=lambda x: lazy_pinyin(x.lower())[0][0])))

    # 根据资料构建词典
    # with open(dictionary_path + "/major.txt", "w", encoding="utf-8") as major_dict:
    #     major_dict.truncate()
    #     for item in major_set4:
    #         major_dict.write(item + "\n")


# 百度百科获取大学专业目录
# noinspection PyProtectedMember
def build_university_major_dict():
    function_logger = MyLog(logger=sys._getframe().f_code.co_name).getlog()
    function_logger.info("构造专业名称词典...")
    source_path = "Information/大学/大学学科(百度百科网页源码).txt"
    with open(source_path, "r", encoding="utf-8") as source_file:
        main_page_source = source_file.read()

    # bs4方法解析尝试
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
    function_logger.info("构造专业名称词典完成")


# 类别词典
# noinspection PyProtectedMember
def build_classy_dict():
    function_logger = MyLog(logger=sys._getframe().f_code.co_name).getlog()
    function_logger.info("构造类别名称词典...")
    classy = ["文科", "理科", "文史", "理工"]
    with open(dictionary_path + "/classy.txt", "w", encoding="utf-8") as classy_dict:
        classy_dict.truncate()
        for item in classy:
            classy_dict.write(item + "\n")
    function_logger.info("构造类别名称词典完成！")


if __name__ == '__main__':
    main_logger = MyLog(logger=__name__).getlog()
    main_logger.info("start...")
    # build_school_dict()
    # build_mysql_major_dict()
    # build_university_major_dict()
    build_classy_dict()
    main_logger.info("end...")
