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

from io import StringIO

from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter,PDFPageAggregator
from pdfminer.layout import LAParams,LTTextBoxHorizontal,LTTextBox,LTTextBoxVertical,LTTextLine,LTTextLineHorizontal,LTTextLineVertical,LTText
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser


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
    mylogger.info("pdf文件读取table完成！")
    return all_tables


def read_pdf_to_text(path):
    mylogger = MyLog(logger=sys._getframe().f_code.co_name).getlog()
    mylogger.info("开始读取pdf文件！")

    # 按页返回页中各个文本
    source_pdf = open(path, 'rb')
    # 创建PDF，资源管理器，来共享资源
    rsrcmgr = PDFResourceManager()
    # 创建一个PDF设备对象
    laparams = LAParams()
    device = PDFPageAggregator(rsrcmgr, laparams=laparams)
    # 创建一个PDF解释其对象
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    # 循环遍历列表，每次处理一个page内容
    # doc.get_pages() 获取page列表
    for page in PDFPage.get_pages(source_pdf):
        interpreter.process_page(page)
        # 接受该页面的LTPage对象
        layout = device.get_result()
        # 这里layout是一个LTPage对象 里面存放着 这个page解析出的各种对象
        # 一般包括LTTextBox, LTFigure, LTImage, LTTextBoxHorizontal 等等
        # 想要获取文本就获得对象的text属性，
        for x in layout:
            if isinstance(x, LTTextBoxHorizontal):
                results = x.get_text()
                print(results)
        print("-----------")
        # print("-------------------")

    mylogger.info("pdf文件读取文本完成！")

    # output = StringIO()
    # # 创建一个PDF资源管理器对象来存储共赏资源
    # pdf_resource_manager = PDFResourceManager()
    # # 创建一个PDF文本设备对象
    # pdf_text_converter = TextConverter(pdf_resource_manager, output, laparams=LAParams())
    # # 创建一个PDF解释器对象
    # pdf_page_interpreter = PDFPageInterpreter(pdf_resource_manager, pdf_text_converter)
    #
    # # 打开源pdf文件
    # source_pdf = open(path, 'rb')
    # pagenums = set()
    # # 对pdf每一页进行分析
    # for page in PDFPage.get_pages(source_pdf, pagenums):
    #     pdf_page_interpreter.process_page(page)
    #     output.write("***\n")
    # source_pdf.close()
    # pdf_text_converter.close()
    #
    # # 得到每一页的txt文档
    # text = output.getvalue()
    # output.close()
    # return text



if __name__ == '__main__':
    mylogger = MyLog(__name__).getlog()
    mylogger.info("start...")
    path = "../InformationGet/Information/九校联盟/南京大学/招生计划/source/2018-安徽.pdf"
    pages = read_pdf_to_tables(path)
    for tables in pages:
        for table in tables:
            for line in table:
                print(line)
            print("--------")
    # for line in text.split("\n"):
    #     print(line)
    # print(text.split("\n"))
    # path = "../InformationGet/Information/九校联盟/上海交通大学/招生计划/source/2018test.pdf"
    # df = tabula.read_pdf(path, encoding="utf-8", pages="all")
    # print(df)
    mylogger.info("end...")