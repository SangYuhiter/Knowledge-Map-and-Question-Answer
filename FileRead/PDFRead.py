# -*- coding: utf-8 -*-
'''
@File  : PDFRead.py
@Author: SangYu
@Date  : 2019/1/9 13:37
@Desc  : PDF读取
'''

import pdfplumber
import tabula
from Log.Logger import MyLog

import sys

def read_pdf_to_tables(path):
    mylogger=MyLog(logger=sys._getframe().f_code.co_name).getlog()
    """
    read pdf and return a table list.
    :param path: the pdf path
    :return tables: table list
    """
    mylogger.info("开始读取pdf文件！")
    with pdfplumber.open(path) as pdf:
        all_tables = []
        for page in pdf.pages:
            tables = page.extract_tables()
            all_tables.append(tables)
    mylogger.info("pdf文件读取完成！")
    return all_tables


if __name__ == '__main__':
    mylogger = MyLog(__name__).getlog()
    mylogger.info("start...")
    path = "../InformationGet/Information/九校联盟/南京大学/录取分数/source/2017-major.pdf"
    pages = read_pdf_to_tables(path)
    print(pages)
    # path = "../InformationGet/Information/九校联盟/上海交通大学/招生计划/source/2018test.pdf"
    # df = tabula.read_pdf(path, encoding="utf-8", pages="all")
    # print(df)
    mylogger.info("end...")