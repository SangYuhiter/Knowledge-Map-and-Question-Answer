# -*- coding: utf-8 -*-
'''
@File  : ImageRead.py
@Author: SangYu
@Date  : 2019/3/4 11:48
@Desc  : 图片读取
'''
import fitz
import os


# 将图片合并为pdf文件
def image_to_pdf(image_list, store_dir, file_name):
    doc = fitz.open()
    for img in sorted(image_list):
        imgdoc = fitz.open(img)  # 打开图片
        pdfbytes = imgdoc.convertToPDF()  # 使用图片创建单页的 PDF
        imgpdf = fitz.open("pdf", pdfbytes)
        doc.insertPDF(imgpdf)
    if os.path.exists(file_name):
        os.remove(file_name)
    doc.save(store_dir + "\\" + file_name)  # 保存pdf文件
    doc.close()

if __name__ == '__main__':
    print("start...")