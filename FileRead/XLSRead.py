# -*- coding: utf-8 -*-
"""
@File  : XLSRead.py
@Author: SangYu
@Date  : 2019/1/10 10:31
@Desc  : 读取.xls文件
"""

import xlrd


def read_xls(file_path):
    """
    解析excel文件
    :param file_path:
    :return: excel解析对象
    """
    excel_file = xlrd.open_workbook(file_path)
    return excel_file


if __name__ == '__main__':
    print("start...")
    path = "../InformationGet/Information/九校联盟/清华大学/招生计划/source/附件：清华大学2012年招生计划.xls"
    file_ = read_xls(path)
    print(file_)
    print("end...")
