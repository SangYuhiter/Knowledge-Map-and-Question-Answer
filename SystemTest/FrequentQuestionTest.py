# -*- coding: utf-8 -*-
'''
@File  : FrequentQuestionTest.py
@Author: SangYu
@Date  : 2019/3/16 19:42
@Desc  : 使用常用问题集对系统进行检测
'''

import os
import csv
import datetime
from QuestionAnalysis.QuestionPretreatment import question_segment_hanlp, question_analysis_to_keyword, \
    question_keyword_normalize, question_abstract, load_question_template
from TemplateLoad.QuestionTemplate import build_mysql_string_by_template
from QuestionQuery.MysqlQuery import mysql_table_query
from InformationGet.MysqlOperation import mysql_query_sentence
import re
from Log.Logger import MyLog
import sys
import time


# 读取文件目录下所有文件（不包含文件夹）
def read_all_file_list(dir_path):
    file_list = []
    for file in os.listdir(dir_path):
        file_path = os.path.join(dir_path, file)
        if os.path.isfile(file_path):
            file_list.append(file_path)
    return file_list


# 读取常用问题
def read_frequent_question():
    mylogger = MyLog(logger=sys._getframe().f_code.co_name).getlog()
    # 常问问题集
    file_path = "../InformationGet/Information/大学/常问问题集"
    file_list = read_all_file_list(file_path)
    for file in file_list:
        school_name = file.split("\\")[-1][:-9]
        mylogger.info("开始读取%s的常问问题集" % school_name)
        with open(file, "r", encoding="utf-8") as csvfile:
            csv_reader = csv.reader(csvfile)
            table_lines = []
            for row in csv_reader:
                table_lines.append(row)
        table_head = table_lines[0]
        table_content = table_lines[1:]
        # 开始进行测试
        mylogger.info("读取完成，开始进行测试！")
        question_count = len(table_content)
        print(question_count)
        answer_notnull_count = 0
        for record in table_content:
            if len(record) == 5:
                question = record[3]
                answer = answer_question(question)
                if answer != ["查询结果为空！"]:
                    answer_notnull_count += 1
                    mylogger.debug("问题:%s" % question)
                    mylogger.debug("回答:%s" % answer)

        with open("record.txt", "a", encoding="utf-8")as record_file:
            now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            record_file.write(now_time+"\n")
            record_file.write("%s总问题数%d/回答不为空数%d\n" % (school_name, question_count, answer_notnull_count))
            mylogger.info("%s总问题数: %d   回答不为空数: %d" % (school_name, question_count, answer_notnull_count))


# 传入问题返回查询结果
def answer_question(question):
    result = question_segment_hanlp(question)
    # print(result)
    keyword = question_analysis_to_keyword(result)
    # print(keyword)
    keyword_normalize = question_keyword_normalize(keyword)
    # print(keyword_normalize)
    result_edit = mysql_table_query(keyword_normalize)
    return result_edit


# 传入问题使用模板回答问题
def answer_question_by_template(question):
    mylogger = MyLog(logger=sys._getframe().f_code.co_name).getlog()
    mylogger.info("使用问题模板回答问题...")
    start_time = time.time()
    # 分词-》提取关键词、抽象问句-》抽象问句匹配模板-》模板构造sql语句-》sql语句返回查询结果-》查询结果构造模板输出
    mylogger.debug("问句：%s" % question)
    segmnet_list = question_segment_hanlp(question)
    mylogger.debug("分词结果：%s" % str(segmnet_list))
    ab_question = question_abstract(segmnet_list)
    mylogger.debug("问题抽象：%s" % ab_question)
    keyword = question_analysis_to_keyword(segmnet_list)
    mylogger.debug("关键词：%s" % str(keyword))
    keyword_normalize = question_keyword_normalize(keyword)
    template_sentence_type = keyword_normalize["search_table"]
    mylogger.debug("正则化关键词：%s" % str(keyword_normalize))
    template_sentence = load_question_template(ab_question, template_sentence_type)
    mylogger.debug("模板句式：%s" % template_sentence)
    template_mysql_string = build_mysql_string_by_template(template_sentence, template_sentence_type)
    mylogger.debug("模板MYSQL语句：%s" % template_mysql_string)
    # 提取槽位
    pattern = re.compile(r"[\(].*?[\)]")
    slots = re.findall(pattern, template_mysql_string)
    mysql_string = template_mysql_string
    for slot in slots:
        key = keyword_normalize["search_"+slot[1:-1]]
        mysql_string = mysql_string.replace(slot, key)
    mylogger.debug("插入关键词后的MYSQL语句：%s" % mysql_string)
    # 数据库查询
    result = mysql_query_sentence(mysql_string)
    result_edit = []
    if len(result) == 0:
        result_edit.append("招生类别查询结果为空！")
    else:
        for item in result:
            result_edit.append(str(item))
    mylogger.debug("数据库查询结果：")
    for item in result_edit:
        mylogger.debug(item)
    end_time = time.time()
    mylogger.debug("查询耗时：%s s" % (end_time - start_time))


if __name__ == '__main__':
    mylogger = MyLog(logger=sys._getframe().f_code.co_name).getlog()
    mylogger.info("start...")
    question = "哈工大前年软件工程在石家庄录取分数？"
    answer_question_by_template(question)
    # read_frequent_question()
    mylogger.info("end...")
