# -*- coding: utf-8 -*-
"""
@File  : DataNormalize.py
@Author: SangYu
@Date  : 2019/3/22 9:50
@Desc  : 数据预处理
"""
from FileRead.FileNameRead import read_all_file_list
from Log.Logger import MyLog
import sys
import csv
import pickle


# 处理常用问题集(csv),问题和答案部分
# noinspection PyProtectedMember,PyShadowingNames,PyDictCreation
def frequent_question_normalize(dir_path: str):
    """
    处理常用问题集(csv),问题和答案部分
    :param dir_path: 文件夹路径
    :return:
    """
    function_logger = MyLog(logger=sys._getframe().f_code.co_name).getlog()
    function_logger.info("开始进行数据处理...")
    file_list = read_all_file_list(dir_path + "/source")
    for file in file_list:
        function_logger.debug(file)
        school_name = file.split("\\")[-1][:-9]
        function_logger.info("开始读取%s的常问问题集..." % school_name)
        with open(file, "r", encoding="utf-8") as csvfile:
            csv_reader = csv.reader(csvfile)
            fqa_lines = []
            for row in csv_reader:
                if len(row) == 5:
                    line = {}
                    line["title"] = row[0].replace(" ", "")
                    line["from"] = row[1]
                    line["time"] = row[2]
                    line["question"] = row[3].replace("\u3000", "").replace("\n", "，").replace(" ", "")
                    line["answer"] = row[4].replace("\ue63c", "").replace("\u3000", "").replace("\n", "，")\
                        .replace(" ", "").lstrip("，")
                    fqa_lines.append(line)
            fqa_lines.pop(0)
        function_logger.info("读取%s的常用问题集完成！" % school_name)
        function_logger.info("开始写入%s的常用问题集..." % school_name)
        with open(dir_path + "/预处理/pickle/" + school_name, "wb")as p_file:
            pickle.dump(fqa_lines, p_file)
        function_logger.info("写入%s的常用问题集完成！" % school_name)
    function_logger.info("数据处理完成！")


if __name__ == '__main__':
    main_logger = MyLog(logger=__name__).getlog()
    main_logger.info("start...")
    question_set_dir = "../InformationGet/Information/大学/常问问题集"
    # frequent_question_normalize(question_set_dir)
    with open(question_set_dir + "/预处理/pickle/" + "上海交通大学医学院", "rb")as p_file:
        data = pickle.load(p_file)
    for q in data[:10]:
        print(q)
    main_logger.info("end...")
