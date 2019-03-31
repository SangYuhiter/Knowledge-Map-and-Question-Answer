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
from TemplateLoad.QuestionTemplate import build_mysql_string_by_template, build_mysql_answer_string_by_template, \
    build_mysql_string_by_template_and_keymap
from QuestionQuery.MysqlQuery import mysql_table_query
from InformationGet.MysqlOperation import mysql_query_sentence
from FileRead.FileNameRead import read_all_file_list
import re
from Log.Logger import MyLog
import sys
import time
import os
from QuestionAnswer.TemplateAnswerQuestion import answer_question_by_template


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
    print(school_name)
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
    answer_count = 0
    answer_null_count = 0
    mysql_string_null_count = 0
    mysql_string_only_school_count = 0
    current_index = 1
    os.chdir(os.path.split(os.path.realpath(__file__))[0])
    if not os.path.exists("record/" + school_name):
        os.makedirs("record/" + school_name)
    with open("record/" + school_name + "/mysql_string_null", "w", encoding="utf-8") as msn_file, \
            open("record/" + school_name + "/mysql_string_only_school", "w", encoding="utf-8") as msos_file, \
            open("record/" + school_name + "/answer_null", "w", encoding="utf-8") as an_file, \
            open("record/" + school_name + "/answer_not_null", "w", encoding="utf-8") as ann_file:
        for record in table_content:
            function_logger.info("%s测试进度%d/%d" % (school_name, question_count, current_index))
            if len(record) == 5:
                question = record[3]
                function_logger.debug(question)
                start_time = time.time()
                mid_result, answer = answer_question_by_template(question, 1, school_name)
                end_time = time.time()
                function_logger.debug("查询时间：%s" % (end_time - start_time))
                function_logger.debug(mid_result["mysql_string"])
                function_logger.debug(answer[0])

                if answer == ["问句条件词为空，无法构建查询语句！"]:
                    mysql_string_null_count += 1
                    msn_file.write(question + "\n")
                    msn_file.write(mid_result["mysql_string"] + "\n")
                    msn_file.write(str(answer) + "\n")
                elif answer == ["问句条件词只有学校，查询过宽！"]:
                    mysql_string_only_school_count += 1
                    msos_file.write(question + "\n")
                    msos_file.write(mid_result["mysql_string"] + "\n")
                    msos_file.write(str(answer) + "\n")
                elif answer == ["查询结果为空！"]:
                    answer_null_count += 1
                    an_file.write(question + "\n")
                    an_file.write(mid_result["mysql_string"] + "\n")
                    an_file.write(str(answer) + "\n")
                else:
                    answer_count += 1
                    # 多余三条的记录只记录前三条和总记录条数
                    ann_file.write(question + "\n")
                    ann_file.write(mid_result["mysql_string"] + "\n")
                    ann_file.write("答案条数：" + str(len(answer)) + "\t")
                    if len(answer) > 3:
                        ann_file.write(str(answer[:3]) + "\n")
                    else:
                        ann_file.write(str(answer) + "\n")
            current_index += 1
        for input_file in [msn_file, msos_file, an_file, ann_file]:
            input_file.write("总问题数%d\t查询语句构造为空数%d\t只有学校关键词数%d\t查询结果为空数%d\t有回答数%d\n" %
                             (question_count, mysql_string_null_count, mysql_string_only_school_count,
                              answer_null_count, answer_count))
    os.chdir(os.path.split(os.path.realpath(__file__))[0])
    with open("record/all.txt", "a", encoding="utf-8")as record_file:
        now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        record_file.write(now_time + "\t" + school_name + "\n")
        record_file.write("总问题数%d\t查询语句构造为空数%d\t只有学校关键词数%d\t查询结果为空数%d\t有回答数%d\n" %
                            (question_count, mysql_string_null_count, mysql_string_only_school_count,
                            answer_null_count, answer_count))



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


if __name__ == '__main__':
    # noinspection PyProtectedMember
    main_logger = MyLog(logger=__name__).getlog()
    main_logger.info("start...")

    # 常问问题集
    file_path = "../InformationGet/Information/大学/常问问题集/预处理"
    file_list = read_all_file_list(file_path)
    for file in file_list:
        test_frequent_question(file)
    main_logger.info("end...")
