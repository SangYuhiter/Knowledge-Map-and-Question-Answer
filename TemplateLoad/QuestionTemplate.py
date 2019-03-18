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
def build_template_by_fields_plan(template_file):
    mylogger = MyLog(logger=sys._getframe().f_code.co_name).getlog()
    mylogger.info("开始构造%s的问题模板..." % template_file.split("/")[-1])
    fields = ["学校", "年份", "专业", "省份", "类别", "人数"]
    fields_en = ["school", "year", "major", "district", "classy", "numbers"]
    template_sentence_ends = ["招生计划？", "招生计划是多少？", "招多少人？", "招生人数？", "招生人数是多少？"]
    with open(template_file, "w", encoding="utf-8") as t_file:
        for field in fields:
            t_file.write(field + "\t")
        t_file.write("\n")
        for field_en in fields_en:
            t_file.write(field_en + "\t")
        t_file.write("\n")
        fields_en_subset = get_subset_binary(fields_en[:-1])
        for subset in fields_en_subset:
            if not subset:
                continue
            else:
                template_sentence = ""
                for field_en in subset:
                    if field_en == "district":
                        template_sentence += "在" + "(" + field_en + ")"
                    elif field_en == "classy":
                        template_sentence += "(" + field_en + ")" + "类考生"
                    else:
                        template_sentence += "(" + field_en + ")"
                for end in template_sentence_ends:
                    t_file.write(template_sentence + end + "\n")
    mylogger.info("%s的问题模板构建完成!" % template_file.split("/")[-1])


# 构造录取分数分省问题模板
def build_template_by_fields_score_pro(template_file):
    mylogger = MyLog(logger=sys._getframe().f_code.co_name).getlog()
    mylogger.info("开始构造%s的问题模板..." % template_file.split("/")[-1])
    fields = ["学校", "年份", "省份", "批次", "类别", "分数线"]
    fields_en = ["school", "year", "district", "batch", "classy", "line"]
    template_sentence_ends = ["录取分数？", "录取分数是多少？", "多少分？", "分数线？", "分数线是多少？"]
    with open(template_file, "w", encoding="utf-8") as t_file:
        for field in fields:
            t_file.write(field + "\t")
        t_file.write("\n")
        for field_en in fields_en:
            t_file.write(field_en + "\t")
        t_file.write("\n")
        fields_en_subset = get_subset_binary(fields_en[:-1])
        for subset in fields_en_subset:
            if not subset:
                continue
            else:
                template_sentence = ""
                for field_en in subset:
                    if field_en == "district":
                        template_sentence += "在" + "(" + field_en + ")"
                    elif field_en == "classy":
                        template_sentence += "(" + field_en + ")" + "类考生"
                    else:
                        template_sentence += "(" + field_en + ")"
                for end in template_sentence_ends:
                    t_file.write(template_sentence + end + "\n")
    mylogger.info("%s的问题模板构建完成!" % template_file.split("/")[-1])


# 构造录取分数分专业问题模板
def build_template_by_fields_score_major(template_file):
    mylogger = MyLog(logger=sys._getframe().f_code.co_name).getlog()
    mylogger.info("开始构造%s的问题模板..." % template_file.split("/")[-1])
    fields = ["学校", "年份", "专业", "省份", "类别", "最高分", "平均分", "最低分", "人数"]
    fields_en = ["school", "year", "major", "district", "classy", "higest", "average", "lowest", "numbers"]
    template_sentence_ends = ["最高分？", "最高分是多少？", "平均分？", "平均分是多少？", "最低分？", "最低分是多少？", "录取人数是多少？"]
    with open(template_file, "w", encoding="utf-8") as t_file:
        for field in fields:
            t_file.write(field + "\t")
        t_file.write("\n")
        for field_en in fields_en:
            t_file.write(field_en + "\t")
        t_file.write("\n")
        fields_en_subset = get_subset_binary(fields_en[:-4])
        for subset in fields_en_subset:
            if not subset:
                continue
            else:
                template_sentence = ""
                for field_en in subset:
                    if field_en == "province":
                        template_sentence += "在" + "(" + field_en + ")"
                    elif field_en == "classy":
                        template_sentence += "(" + field_en + ")" + "类考生"
                    else:
                        template_sentence += "(" + field_en + ")"
                for end in template_sentence_ends:
                    t_file.write(template_sentence + end + "\n")
    mylogger.info("%s的问题模板构建完成!" % template_file.split("/")[-1])


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


# 通过问题模板文件加载问题模板
def load_template_by_file(file_path):
    with open(file_path, "r", encoding="utf-8") as t_file:
        lines = t_file.readlines()
        # 读取模板词（中英文）
        fields = lines[0].split("\t")[:-1]
        fields_en = lines[1].split("\t")[:-1]
        template_sentence = [item.replace("\n", "") for item in lines[2:]]
        return fields, fields_en, template_sentence

if __name__ == '__main__':
    mylogger = MyLog(logger=__name__).getlog()
    mylogger.info("start...")
    # build_mysql_string_by_template("(school)(year)(major)在(province)招生人数是多少？")
    # print(build_mysql_string_by_template("(school)(year)(major)在(province)招生人数是多少？"))
    # template_path = "Template"
    # load_template_by_file(template_path + "/admission_plan")
    template_path = "Template"
    build_template_by_fields(template_path + "/admission_score_major")
    mylogger.info("end...")
