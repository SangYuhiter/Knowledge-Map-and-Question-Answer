# -*- coding: utf-8 -*-
'''
@File  : PDFRead.py
@Author: SangYu
@Date  : 2019/1/9 13:37
@Desc  : PDF读取
'''

import pdfplumber
import pandas as pd

def read_pdf_to_tables(path):
    """
    read pdf and return a table list.
    :param path: the pdf path
    :return tables: table list
    """
    with pdfplumber.open(path) as pdf:
        all_tables = []
        for page in pdf.pages:
            tables = page.extract_tables()
            all_tables.append(tables)
    return all_tables

if __name__ == '__main__':
    path = "../InformationGet/Information/九校联盟/清华大学/招生计划/source/附件：清华大学2013年招生计划.pdf"
    read_pdf_to_tables(path)