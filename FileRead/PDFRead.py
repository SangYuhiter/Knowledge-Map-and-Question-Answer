# -*- coding: utf-8 -*-
"""
@File  : PDFRead.py
@Author: SangYu
@Date  : 2019/1/9 13:37
@Desc  : PDF读取
"""
import pdfplumber
from Log.Logger import MyLog
import sys


# noinspection PyProtectedMember
def read_pdf_to_tables(file_path):
    """
    解析pdf文件中的表格
    :param file_path: pdf文件路径
    :return: 表格数据列表
    """
    function_logger = MyLog(logger=sys._getframe().f_code.co_name).getlog()
    function_logger.info("开始读取pdf文件！")
    with pdfplumber.open(path) as pdf:
        all_tables = []
        # 对每一页pdf中的表格进行解析并添加到列表结构中
        for page in pdf.pages:
            tables = page.extract_tables()
            all_tables.append(tables)
    function_logger.info("pdf文件读取table完成！")
    return all_tables


if __name__ == '__main__':
    main_logger = MyLog(__name__).getlog()
    main_logger.info("start...")
    path = "../InformationGet/Information/九校联盟/清华大学/招生计划/source/附件：清华大学2013年招生计划.pdf"
    pages = read_pdf_to_tables(path)
    print(pages)
    main_logger.info("end...")
