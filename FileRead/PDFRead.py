# -*- coding: utf-8 -*-
"""
@File  : PDFRead.py
@Author: SangYu
@Date  : 2019/1/9 13:37
@Desc  : PDF读取
"""
import fitz
import pdfplumber
import tabula
from Log.Logger import MyLog
import sys

from io import StringIO

from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter, PDFPageAggregator
from pdfminer.layout import LAParams, LTTextBoxHorizontal, LTTextBox, LTTextBoxVertical, LTTextLine, \
    LTTextLineHorizontal, LTTextLineVertical, LTText
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser


# noinspection PyProtectedMember
def read_pdf_to_tables(path):
    function_logger = MyLog(logger=sys._getframe().f_code.co_name).getlog()
    """
    read pdf and return a table list.
    :param path: the pdf path
    :return tables: table list
    """
    function_logger.info("开始读取pdf文件！")
    with pdfplumber.open(path) as pdf:
        all_tables = []
        for page in pdf.pages:
            tables = page.extract_tables()
            all_tables.append(tables)
    function_logger.info("pdf文件读取table完成！")
    return all_tables


# noinspection PyProtectedMember
def read_pdf_to_words(path):
    function_logger = MyLog(logger=sys._getframe().f_code.co_name).getlog()
    function_logger.info("开始读取pdf文件！")
    with pdfplumber.open(path) as pdf:
        all_words = []
        for page in pdf.pages:
            words = page.extract_words()
            all_words.append(words)
    function_logger.info("pdf文件读取table完成！")
    return all_words


# noinspection PyProtectedMember
def read_pdf_to_text(path):
    function_logger = MyLog(logger=sys._getframe().f_code.co_name).getlog()
    function_logger.info("开始读取pdf文件！")

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

    function_logger.info("pdf文件读取文本完成！")

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


# 切分单页pdf
# noinspection PyUnresolvedReferences
def split_pdf_single_page(path):
    src = fitz.open(path)
    doc = fitz.open()
    # page = doc.newPage(width=src[0].rect.width,
    #                     height=src[0].rect.height + src[0].rect.height)
    # page.showPDFpage(src[0].rect, src, 0)
    # placerect = fitz.Rect([0, src[0].rect[3], src[0].rect[2], src[0].rect[3] + src[0].rect[3]])
    # page.showPDFpage(placerect, src, 0, clip=src[0].rect)
    # doc.save('split/new.pdf', garbage=4, deflate=True)
    # for page in src:
    #     r = page.rect
    #     page1 = doc.newPage(width=r.width/2, height=r.height)
    #
    #     page.showPDFpage(page.rect, src, 0)
    #     doc.save("split/cut1.pdf")
    for i_page in range(len(src)):
        r = src[i_page].rect
        d = fitz.Rect(src[i_page].CropBoxPosition, src[i_page].CropBoxPosition)
        # cut1 = fitz.Rect(0,0,r.width, r.height)
        cut2 = d + (0, 0, r.width / 2, r.height)
        page1 = doc.newPage(width=cut2.width, height=cut2.height)
        page1.showPDFpage(src[i_page].rect, src, i_page)
    doc.save("split/poster-" + src.name, garbage=3, deflate=True)


if __name__ == '__main__':
    main_logger = MyLog(__name__).getlog()
    main_logger.info("start...")
    # path = "../InformationGet/Information/九校联盟/上海交通大学/招生计划/source/20150.pdf"
    # pages = read_pdf_to_tables(path)
    # test_path = "enhance/all_image.pdf"
    # read_pdf_to_text(test_path)
    split_pdf_single_page("test_pdf.pdf")
    # for tables in pages:
    #     for table in tables:
    #         for line in table:
    #             print(line)
    #         print("--------")
    # for line in text.split("\n"):
    #     print(line)
    # print(text.split("\n"))
    # path = "../InformationGet/Information/九校联盟/上海交通大学/招生计划/source/2018test.pdf"
    # df = tabula.read_pdf(path, encoding="utf-8", pages="all")
    # print(df)
    main_logger.info("end...")
