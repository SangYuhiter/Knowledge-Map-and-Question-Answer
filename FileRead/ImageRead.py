# -*- coding: utf-8 -*-
"""
@File  : ImageRead.py
@Author: SangYu
@Date  : 2019/3/4 11:48
@Desc  : 图片读取
"""
import fitz
import os
# import skimage
from skimage import io, morphology
from FileRead.FileNameRead import read_all_file_list
import tesserocr
from PIL import Image, ImageEnhance


# 将图片合并为pdf文件
# noinspection PyUnresolvedReferences
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


# pdf转图片
# noinspection PyUnresolvedReferences
def pdf_to_image(path):
    doc = fitz.open(path)
    for page in doc:
        pix = page.getPixmap(alpha=False)
        pix.writePNG("page-%i.png" % page.number)


# 图片切割
def image_cut(path):
    img = Image.open(path)
    img_size = img.size
    h = img_size[1]
    w = img_size[0]
    mid = w // 2
    cut1 = img.crop((0, 0, mid, h))
    cut1.save("cut1.jpg")
    cut2 = img.crop((mid, 0, w, h))
    cut2.save("cut2.jpg")


# 图片增强
def img_enhance(path):
    image = Image.open(path)
    # image.show()
    enh_con = ImageEnhance.Contrast(image)
    contrast = 1.5
    image_contrasted = enh_con.enhance(contrast)
    # image_contrasted.show()
    image_contrasted.save("enhance/" + path.split("/")[-1])


# 识别表格图像
def read_table_img(img_path):
    # 读取图片，并转灰度图
    img = io.imread(img_path, as_gray=True)
    # 二值化
    bi_th = 0.81
    img[img <= bi_th] = 0
    img[img > bi_th] = 1
    return img


# 膨胀腐蚀操作
def dil2ero(img, selem):
    img = morphology.dilation(img, selem)  # 灰度膨胀（（i,j）处值为领域最大值）
    imgres = morphology.erosion(img, selem)  # 灰度腐蚀
    return imgres


# 求图像中的横线和竖线
def get_col_row(img):
    rows, cols = img.shape
    scale = 80
    col_selem = morphology.rectangle(cols // scale, 1)
    img_cols = dil2ero(img, col_selem)
    row_selem = morphology.rectangle(1, rows // scale)
    img_rows = dil2ero(img, row_selem)
    return img_cols, img_rows


# tesserocr test
def tesserocr_img(path):
    image = Image.open(path)
    print(tesserocr.image_to_text(image))


if __name__ == '__main__':
    print("start...")
    file_list = read_all_file_list("enhance")
    image_to_pdf(file_list, "enhance", "all_image.pdf")
    # pdf_to_image("test/test1.pdf")
    # image_cut("test/page-0.png")
    # img_enhance("cut/cut1.jpg")
    # img_enhance("cut/cut2.jpg")
    # skimage.io.use_plugin('matplotlib','imshow')
    # path = "../InformationGet/Information/九校联盟/上海交通大学/招生计划/source/20150.jpg"
    # path = "testyiliao2.jpg"
    # img = read_table_img(path)
    # img_cols,img_rows = get_col_row(img)
    # # 线图
    # img_line = img_cols*img_rows
    # # 点图
    # img_dot = img_cols + img_rows
    # io.imshow(img_line)
    # io.show()
    # tesserocr_img('test.png')
    print("end...")
