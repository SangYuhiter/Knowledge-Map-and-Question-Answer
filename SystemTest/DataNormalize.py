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


# 处理常用问题集(csv),问题和答案部分
# noinspection PyProtectedMember
def frequent_question_normalize(dir_path: str):
    """
    处理常用问题集(csv),问题和答案部分
    :param dir_path: 文件夹路径
    :return:
    """
    function_logger = MyLog(logger=sys._getframe().f_code.co_name).getlog()
    function_logger.info("开始进行数据处理...")
    file_list = read_all_file_list(dir_path)
    for file in file_list:
        function_logger.debug(file)
        school_name = file.split("\\")[-1][:-9]
        function_logger.info("开始读取%s的常问问题集..." % school_name)
        with open(file, "r", encoding="utf-8") as csvfile:
            csv_reader = csv.reader(csvfile)
            table_lines = []
            for row in csv_reader:
                table_lines.append(row)
        table_head = table_lines[0]
        table_content = table_lines[1:]
        function_logger.debug(str(table_head))
        for i_line in range(len(table_content)):
            if len(table_content[i_line]) == 5:
                table_content[i_line][-1] = table_content[i_line][-1] \
                    .replace("\ue63c", "").replace("\u3000", "").replace("\n", "，").replace(" ", "").lstrip("，")
                table_content[i_line][-2] = table_content[i_line][-2] \
                    .replace("\u3000", "").replace("\n", "，").replace(" ", "")
                if "贵校" in table_content[i_line][-2]:
                    table_content[i_line][-2] = table_content[i_line][-2].replace("贵校", school_name)
                else:
                    table_content[i_line][-2] = school_name + "，" + table_content[i_line][-2]
                function_logger.debug(str(table_content[i_line]))
        function_logger.info("读取%s的常用问题集完成！" % school_name)
        function_logger.info("开始写入%s的常用问题集..." % school_name)
        with open(dir_path + "/预处理/" + school_name + "常用问题集(预处理).csv", "w", newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(table_head)
            for line in table_content:
                writer.writerow(line)
        function_logger.info("写入%s的常用问题集完成！" % school_name)
    function_logger.info("数据处理完成！")


if __name__ == '__main__':
    main_logger = MyLog(logger=__name__).getlog()
    main_logger.info("start...")
    question_set_dir = "../InformationGet/Information/大学/常问问题集"
    frequent_question_normalize(question_set_dir)
    main_logger.info("end...")
