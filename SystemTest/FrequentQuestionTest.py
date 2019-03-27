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
from TemplateLoad.QuestionTemplate import build_mysql_string_by_template, build_mysql_answer_string_by_template,build_mysql_string_by_template_and_keymap
from QuestionQuery.MysqlQuery import mysql_table_query
from InformationGet.MysqlOperation import mysql_query_sentence
from FileRead.FileNameRead import read_all_file_list
import re
from Log.Logger import MyLog
import sys
import time


# 读取常用问题
# noinspection PyProtectedMember
def test_frequent_question(file_path: str):
    """
    读取常用问题集文件，并进行测试
    :param file_path: 文件（csv）路径
    :return:
    """
    function_logger = MyLog(logger=sys._getframe().f_code.co_name).getlog()
    school_name = file.split("\\")[-1][:-14]
    function_logger.info("开始读取%s的常问问题集" % school_name)
    with open(file, "r", encoding="utf-8") as csvfile:
        csv_reader = csv.reader(csvfile)
        table_lines = []
        for row in csv_reader:
            table_lines.append(row)
    table_head = table_lines[0]
    table_content = table_lines[1:]
    # print(table_head)
    # for line in table_content:
    #     print(line)
    # 开始进行测试
    function_logger.info("读取完成，开始进行测试！")
    question_count = len(table_content)
    print(question_count)
    answer_null_count = 0
    mysql_string_null_count = 0
    current_index = 1
    with open("record/" + school_name, "w", encoding="utf-8") as s_file:
        for record in table_content[:200]:
            function_logger.info("%s测试进度%d/%d" % (school_name, question_count, current_index))
            if len(record) == 5:
                question = record[3]
                mid_result, answer = answer_question_by_template(question)
                if answer == ["查询结果为空！"]:
                    answer_null_count += 1
                elif answer == ["问句条件词不够，无法构建查询语句"]:
                    mysql_string_null_count += 1
                s_file.write(question + "\n")
                s_file.write(mid_result["mysql_string"] + "\n")
                # 多余三条的记录只记录前三条和总记录条数
                s_file.write("答案条数：" + str(len(answer)) + "\t")
                if len(answer) > 3:
                    s_file.write(str(answer[:3]) + "\n")
                else:
                    s_file.write(str(answer)+"\n")
            time.sleep(3)
            current_index += 1
        s_file.write("总问题数%d\t查询语句构造为空数%d\t回答为空数%d\t\n" % (question_count, mysql_string_null_count, answer_null_count))

    with open("record.txt", "a", encoding="utf-8")as record_file:
        now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        record_file.write(now_time + "\n")
        record_file.write("总问题数%d\t查询语句构造为空数%d\t回答为空数%d\t\n" % (question_count, mysql_string_null_count, answer_null_count))


# 传入问题返回查询结果（原始版本）
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
    # 保存中间结果
    mid_result = {}
    segment_list = question_segment_hanlp(question)
    mid_result["segment_list"] = segment_list
    ab_question = question_abstract(segment_list)
    mid_result["ab_question"] = ab_question
    keyword = question_analysis_to_keyword(segment_list)
    mid_result["keyword"] = keyword
    keyword_normalize = question_keyword_normalize(keyword)
    mid_result["keyword_normalize"] = keyword_normalize
    template_sentence_type = keyword_normalize["search_table"]
    fq_condition, fq_target, match_template_question, match_template_answer \
        = find_question_match_template(ab_question, template_sentence_type)
    mid_result["match_template_question"] = match_template_question
    mid_result["match_template_answer"] = match_template_answer
    mysql_string = build_mysql_string_by_template_and_keymap(match_template_question, template_sentence_type,
                                                             keyword_normalize)
    mid_result["mysql_string"] = mysql_string
    # 数据库查询
    result = []
    result_edit = []
    if mysql_string == "":
        result_edit.append("问句条件词不够，无法构建查询语句")
    else:
        result = mysql_query_sentence(mysql_string)
        if len(result) == 0:
            result_edit.append("查询结果为空！")
        else:
            mid_result["search_result"] = result
            for item in result:
                answer_string = build_mysql_answer_string_by_template(match_template_answer, item)
                result_edit.append(answer_string)
    return mid_result, result_edit


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
    mysql_string = build_mysql_string_by_template_and_keymap(match_template_question, template_sentence_type, keyword_normalize)
    function_logger.debug("mysql语句："+mysql_string)
    # 数据库查询
    result = []
    result_edit = []
    if mysql_string == "":
        result_edit.append("问句条件词不够，无法构建查询语句")
    else:
        result = mysql_query_sentence(mysql_string)
        if len(result) == 0:
            result_edit.append("查询结果为空！")
        else:
            for item in result:
                answer_string = build_mysql_answer_string_by_template(match_template_answer, item)
                result_edit.append(answer_string)
        function_logger.debug("数据库查询结果：")
        for item in result_edit:
            function_logger.debug(item)
        end_time = time.time()
        function_logger.debug("查询耗时：%s s" % (end_time - start_time))
    return result_edit


if __name__ == '__main__':
    # noinspection PyProtectedMember
    main_logger = MyLog(logger=__name__).getlog()
    main_logger.info("start...")
    # test_question = "哈工大前年软件工程石家庄招生人数？"
    # test_result = answer_question_by_template(test_question)
    # print(test_result)

    # 常问问题集
    file_path = "../InformationGet/Information/大学/常问问题集/预处理"
    file_list = read_all_file_list(file_path)
    for file in file_list[-3:]:
        test_frequent_question(file)
    main_logger.info("end...")
