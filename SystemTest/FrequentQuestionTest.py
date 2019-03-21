# -*- coding: utf-8 -*-
"""
@File  : FrequentQuestionTest.py
@Author: SangYu
@Date  : 2019/3/16 19:42
@Desc  : 使用常用问题集对系统进行检测
"""
import csv
import datetime
from QuestionAnalysis.QuestionPretreatment import question_segment_hanlp, question_analysis_to_keyword, \
    question_keyword_normalize, question_abstract, find_question_match_template
from TemplateLoad.QuestionTemplate import build_mysql_string_by_template, build_mysql_answer_string_by_template
from QuestionQuery.MysqlQuery import mysql_table_query
from InformationGet.MysqlOperation import mysql_query_sentence
from FileRead.FileNameRead import read_all_file_list
import re
from Log.Logger import MyLog
import sys
import time


# 读取常用问题
# noinspection PyProtectedMember
def read_frequent_question():
    function_logger = MyLog(logger=sys._getframe().f_code.co_name).getlog()
    # 常问问题集
    file_path = "../InformationGet/Information/大学/常问问题集"
    file_list = read_all_file_list(file_path)
    for file in [file_list[0]]:
        school_name = file.split("\\")[-1][:-9]
        function_logger.info("开始读取%s的常问问题集" % school_name)
        with open(file, "r", encoding="utf-8") as csvfile:
            csv_reader = csv.reader(csvfile)
            table_lines = []
            for row in csv_reader:
                table_lines.append(row)
        # table_head = table_lines[0]
        table_content = table_lines[1:]
        # 开始进行测试
        function_logger.info("读取完成，开始进行测试！")
        question_count = len(table_content)
        print(question_count)
        answer_notnull_count = 0
        with open("record/" + school_name, "w", encoding="utf-8") as s_file:
            for record in table_content:
                if len(record) == 5:
                    question = record[3].replace("\n", "").replace(" ", "")
                    answer = answer_question_by_template(question)
                    if answer != ["查询结果为空！"]:
                        answer_notnull_count += 1
                        s_file.write(question + "\n")
                        s_file.write(str(answer) + "\n")
                time.sleep(1)

        with open("record.txt", "a", encoding="utf-8")as record_file:
            now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            record_file.write(now_time + "\n")
            record_file.write("%s总问题数%d/回答不为空数%d\n" % (school_name, question_count, answer_notnull_count))
            function_logger.info("%s总问题数: %d   回答不为空数: %d" % (school_name, question_count, answer_notnull_count))


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
    # 分词-》提取关键词、抽象问句-》抽象问句匹配模板-》模板构造sql语句-》sql语句返回查询结果-》查询结果构造模板输出
    segmnet_list = question_segment_hanlp(question)
    ab_question = question_abstract(segmnet_list)
    keyword = question_analysis_to_keyword(segmnet_list)
    keyword_normalize = question_keyword_normalize(keyword)
    template_sentence_type = keyword_normalize["search_table"]
    fq_condition, fq_target, match_template_question, match_template_answer \
        = find_question_match_template(ab_question, template_sentence_type)
    template_mysql_string = build_mysql_string_by_template(match_template_question, template_sentence_type)
    # 提取槽位
    pattern = re.compile(r"[(].*?[)]")
    slots = re.findall(pattern, template_mysql_string)
    mysql_string = template_mysql_string
    for slot in slots:
        key = keyword_normalize["search_" + slot[1:-1]]
        mysql_string = mysql_string.replace(slot, key)
    # 数据库查询
    result = mysql_query_sentence(mysql_string)
    result_edit = []
    if len(result) == 0:
        result_edit.append("查询结果为空！")
    else:
        for item in result:
            answer_string = build_mysql_answer_string_by_template(match_template_answer, item)
            result_edit.append(answer_string)
    return result_edit


# 传入问题使用模板回答问题(测试使用)
# noinspection PyProtectedMember
def answer_question_by_template_test(question):
    function_logger = MyLog(logger=sys._getframe().f_code.co_name).getlog()
    function_logger.info("使用问题模板回答问题...")
    start_time = time.time()
    # 分词-》提取关键词、抽象问句-》抽象问句匹配模板-》模板构造sql语句-》sql语句返回查询结果-》查询结果构造模板输出
    function_logger.debug("问句：%s" % question)
    segmnet_list = question_segment_hanlp(question)
    function_logger.debug("分词结果：%s" % str(segmnet_list))
    ab_question = question_abstract(segmnet_list)
    function_logger.debug("问题抽象：%s" % ab_question)
    keyword = question_analysis_to_keyword(segmnet_list)
    function_logger.debug("关键词：%s" % str(keyword))
    keyword_normalize = question_keyword_normalize(keyword)
    template_sentence_type = keyword_normalize["search_table"]
    function_logger.debug("正则化关键词：%s" % str(keyword_normalize))
    fq_condition, fq_target, match_template_question, match_template_answer \
        = find_question_match_template(ab_question, template_sentence_type)
    function_logger.debug(str(fq_condition))
    function_logger.debug(str(fq_target))
    function_logger.debug("模板句式：%s" % match_template_question)
    function_logger.debug("答案句式：%s" % match_template_answer)
    template_mysql_string = build_mysql_string_by_template(match_template_question, template_sentence_type)
    function_logger.debug("模板MYSQL语句：%s" % template_mysql_string)
    # 提取槽位
    pattern = re.compile(r"[(].*?[)]")
    slots = re.findall(pattern, template_mysql_string)
    mysql_string = template_mysql_string
    for slot in slots:
        key = keyword_normalize["search_" + slot[1:-1]]
        mysql_string = mysql_string.replace(slot, key)
    function_logger.debug("插入关键词后的MYSQL语句：%s" % mysql_string)
    # 数据库查询
    result = mysql_query_sentence(mysql_string)
    result_edit = []
    if len(result) == 0:
        result_edit.append("查询结果为空！")
    else:
        for item in result:
            result_edit.append(str(item))
            answer_string = build_mysql_answer_string_by_template(match_template_answer, item)
            result_edit.append(answer_string)
    function_logger.debug("数据库查询结果：")
    for item in result_edit:
        function_logger.debug(item)
    end_time = time.time()
    function_logger.debug("查询耗时：%s s" % (end_time - start_time))


if __name__ == '__main__':
    # noinspection PyProtectedMember
    main_logger = MyLog(logger=__name__).getlog()
    main_logger.info("start...")
    test_question = "哈工大前年软件工程石家庄招生人数？"
    test_result = answer_question_by_template(test_question)
    print(test_result)
    # read_frequent_question()
    main_logger.info("end...")
