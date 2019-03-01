# -*- coding: utf-8 -*-
'''
@File  : XLSRead.py
@Author: SangYu
@Date  : 2019/1/10 10:31
@Desc  : 读取.xls文件
'''

import xlrd
def read_xls(path):
    ExcelFile = xlrd.open_workbook(path)
    return ExcelFile
if __name__ == '__main__':
    print("start...")
    path ="../InformationGet/Information/九校联盟/清华大学/招生计划/source/附件：清华大学2012年招生计划.xls"
    read_xls(path)
    print("end...")