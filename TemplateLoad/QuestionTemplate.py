# -*- coding: utf-8 -*-
'''
@File  : QuestionTemplate.py
@Author: SangYu
@Date  : 2019/3/16 10:27
@Desc  : 问题模板
'''
from Log.Logger import MyLog
import sys
from FileRead.FileNameRead import read_all_file_list
from openpyxl import load_workbook
import re


# 求列表元素的子集(二进制法)
# print(get_subset_binary([1, 2, 3]))
def get_subset_binary(item):
    n = len(item)
    sub_set = []
    for i in range(2 ** n):
        tem_set = []
        for j in range(n):
            if (i >> j) % 2 == 1:
                tem_set.append(item[j])
        sub_set.append(tem_set)
    return sub_set


# 通过excel表格加载表格内容
# file_path = "../InformationGet/Information/哈工大招生办/招办数据0605"
# file_list = read_all_file_list(file_path)
# for file in [file_list[0]]:
#     build_question_template(file)
def build_question_template(file_path):
    mylogger = MyLog(logger=sys._getframe().f_code.co_name).getlog()
    # 加载excel表格
    mylogger.info("加载表格:%s" % file_path.split("\\")[-1])
    wb = load_workbook(file_path)
    sheet_names = wb.sheetnames
    sheet_first = wb.get_sheet_by_name(sheet_names[0])
    table_head = []
    for item in range(1, sheet_first.max_column + 1):
        table_head.append(sheet_first.cell(row=1, column=item).value)
    mylogger.debug("表头:%s" % str(table_head))
    table_attr = {}
    for i_column in range(1, sheet_first.max_column + 1):
        column_name = sheet_first.cell(row=1, column=i_column).value
        column_value = set()
        for i_row in range(2, sheet_first.max_row + 1):
            column_value.add(sheet_first.cell(row=i_row, column=i_column).value)
        table_attr[column_name] = str(list(column_value))
    for key in table_attr:
        mylogger.debug(key)
        value_list = [value.replace("'", "").strip() for value in table_attr[key][1:-1].split(",")]
        value_list.sort()
        mylogger.debug("列表长度:%d" % len(value_list))
        mylogger.debug(str(value_list))
    mylogger.info("加载表格:%s完成!" % file_path.split("\\")[-1])


# 通过规定字段构造模板
def build_template_by_fields(template_file):
    mylogger = MyLog(logger=sys._getframe().f_code.co_name).getlog()
    mylogger.info("开始构造模板...")
    # 根据表名分别进行模板构造
    if "admission_plan" in template_file:
        build_template_by_fields_plan(template_file)
    elif "admission_score_pro" in template_file:
        build_template_by_fields_score_pro(template_file)
    elif "admission_score_major" in template_file:
        build_template_by_fields_score_major(template_file)


# 构造招生计划问题模板
# noinspection PyProtectedMember
def build_template_by_fields_plan(template_path: str):
    """
    构造招生计划问题模板
    :param template_path: 模板路径
    :return:
    """
    fields_question_condition = ["school 学校", "year 年份", "major 专业", "district 省份", "classy 类别"]
    fields_question_target = ["numbers 招生人数 招生计划 招多少人 招生计划是多少 招生人数是多少"]
    template_sentence_questions = ["(school)(year)(major)(district)(classy)(numbers)"]
    template_sentence_answers = ["(school)(year)(major)(district)招收(classy)(numbers)人"]
    build_template_by_infos(template_path, fields_question_condition, fields_question_target,
                            template_sentence_questions, template_sentence_answers)


# 构造录取分数分省问题模板
def build_template_by_fields_score_pro(template_path: str):
    """
    构造录取分数分省问题模板
    :param template_path: 模板路径
    :return:
    """
    fields_question_condition = ["school 学校", "year 年份", "district 省份 地区", "batch 批次", "classy 类别"]
    fields_question_target = ["line 分数线 录取分数 多少分 录取分数是多少 分数线是多少"]
    template_sentence_questions = ["(school)(year)(district)(batch)(classy)(line)"]
    template_sentence_answers = ["(school)(year)(district)(batch)(classy)录取分数是(line)"]
    build_template_by_infos(template_path, fields_question_condition, fields_question_target,
                            template_sentence_questions, template_sentence_answers)


# 构造录取分数分专业问题模板
def build_template_by_fields_score_major(template_path: str):
    """

    :param template_path: 模板路径
    :return:
    """
    fields_question_condition = ["school 学校", "year 年份", "major 专业", "district 省份 地区",  "classy 类别"]
    fields_question_target = ["highest 最高分 最高分是多少",
                              "average 平均分 平均分是多少",
                              "lowest 最低分 最低分是多少 分数线 分数线是多少",
                              "amount 录取人数 录取多少人"]
    template_sentence_questions = ["(school)(year)(major)(district)(classy)(highest)",
                                   "(school)(year)(major)(district)(classy)(average)",
                                   "(school)(year)(major)(district)(classy)(lowest)",
                                   "(school)(year)(major)(district)(classy)(amount)"]
    template_sentence_answers = ["(school)(year)(major)(district)(classy)最高分是(highest)",
                                 "(school)(year)(major)(district)(classy)平均分是(average)",
                                 "(school)(year)(major)(district)(classy)最低分是(lowest)",
                                 "(school)(year)(major)(district)(classy)录取人数是(amount)"]
    build_template_by_infos(template_path, fields_question_condition, fields_question_target,
                            template_sentence_questions, template_sentence_answers)


# 构造问题模板（提供模板名字段和完整的模板句示例）
# noinspection PyProtectedMember
def build_template_by_infos(template_path: str, fields_question_condition: list, fields_question_target: list,
                            template_sentence_questions: list, template_sentence_answers: list):
    """
    通过提供的信息构造问题模板
    :param template_path: 模板路径
    :param fields_question_condition: 问句条件词，例["school 学校", "year 年份", "major 专业", "district 省份", "classy 类别"]
    :param fields_question_target: 问句目标词，例["numbers 招生人数 招生计划 招多少人 招生计划是多少 招生人数是多少"]
    :param template_sentence_questions: 模板问题句
    :param template_sentence_answers: 模板答案句
    :return:
    """
    function_logger = MyLog(logger=sys._getframe().f_code.co_name).getlog()
    function_logger.info("开始构造%s的问题模板..." % template_path.split("\\")[-1])
    with open(template_path, "w", encoding="utf-8") as t_file:
        # 写入问句条件词数量、中英文对应字段，并获取英文字段列表，用于构造问句
        t_file.write(str(len(fields_question_condition)) + "\n")
        template_fields_en = []
        for fq_condition in fields_question_condition:
            template_fields_en.append(fq_condition.split(" ")[0])
            t_file.write(fq_condition+"\n")
        # 写入问句目标词数量、中英文对应字段
        t_file.write(str(len(fields_question_target)) + "\n")
        for fq_target in fields_question_target:
            t_file.write(fq_target+"\n")
        # 写入模板答句
        t_file.write(str(len(template_sentence_answers)) + "\n")
        for ts_answer in template_sentence_answers:
            t_file.write(ts_answer + "\n")
        # 利用问句条件词英文字段构造子集，使用替换的方法构造所有全排列的问句
        fields_en_subset = get_subset_binary(template_fields_en)
        for i_question in range(len(template_sentence_questions)):
            # 查询当前问句的问句目标词
            match_question_target = []
            for fq_target in fields_question_target:
                if fq_target.split(" ")[0] in template_sentence_questions[i_question]:
                    match_question_target = fq_target.split(" ")
                    break
            # 对问句目标词中对应的每一个询问方式进行替换
            target_word = match_question_target[0]
            for question_mode in match_question_target[1:]:
                # 对子集中的每一个集合进行替换
                for subset in fields_en_subset:
                    sentence = template_sentence_questions[i_question].replace("(" + target_word + ")", question_mode) \
                               + "--" + str(i_question)
                    # 子集为空，不缺省参数
                    if not subset:
                        t_file.write(sentence + "\n")
                    # 子集为原集合，不添加
                    elif len(subset) == len(template_fields_en):
                        continue
                    # 子集有缺省，去除子集中的元素后再添加
                    else:
                        for field_en in subset:
                            sentence = sentence.replace("("+field_en+")", "")
                        t_file.write(sentence + "\n")
    function_logger.info("%s的问题模板构建完成!" % template_path.split("\\")[-1])


# 通过模板类型（槽位）构造MySQL语句
def build_mysql_string_by_template(template_sentence, template_sentence_type):
    mylogger = MyLog(logger=sys._getframe().f_code.co_name).getlog()
    mylogger.info("开始构造MySQL语句...")
    search_table = template_sentence_type
    # 提取模板句中的槽
    pattern = re.compile(r"[\(].*?[\)]")
    slots = re.findall(pattern, template_sentence)
    # print(slots)
    # 构造SQL语句
    mysql_string = "select * from " + search_table + " where "

    for i_slot in range(len(slots)):
        if i_slot == len(slots)-1:
            mysql_string += slots[i_slot][1:-1] + "='" + slots[i_slot] + "'"
        else:
            mysql_string += slots[i_slot][1:-1]+"='"+slots[i_slot]+"' and "
    mysql_string += ";"
    mylogger.info("MySQL语句构造完成！")
    return mysql_string


# 通过模板类型（槽位）构造答句
def build_answer_string_by_template(template_sentence_answer,fields_en,query_result_item):
    # 提取槽位
    pattern = re.compile(r"[\(].*?[\)]")
    slots = re.findall(pattern, template_sentence_answer)
    answer_string = template_sentence_answer
    for slot in slots:
        answer_key = query_result_item[fields_en.index(slot[1:-1])+1]
        answer_string = answer_string.replace(slot, str(answer_key))
    return answer_string


# 通过问题模板文件加载问题模板
def load_template_by_file(file_path):
    with open(file_path, "r", encoding="utf-8") as t_file:
        lines = t_file.readlines()
        # 读取模板词（中英文）
        fields = lines[0].split("\t")[:-1]
        fields_en = lines[1].split("\t")[:-1]
        # 答句数
        sentence_answer_count = int(lines[2].strip())
        template_sentence_answer = [item.replace("\n", "") for item in lines[3:3+sentence_answer_count]]
        template_sentence = [item.replace("\n", "") for item in lines[3+sentence_answer_count:]]
        return fields, fields_en, template_sentence_answer, template_sentence


if __name__ == '__main__':
    mylogger= MyLog(logger=__name__).getlog()
    mylogger.info("start...")
    # build_mysql_string_by_template("(school)(year)(major)在(province)招生人数是多少？")
    # print(build_mysql_string_by_template("(school)(year)(major)在(province)招生人数是多少？"))
    # template_path = "Template"
    # load_template_by_file(template_path + "/admission_plan")
    test_template_path = "Template"
    build_template_by_fields(test_template_path + "/admission_score_major")
    mylogger.info("end...")
