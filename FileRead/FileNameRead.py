# -*- coding: utf-8 -*-
"""
@File  : FileNameRead.py
@Author: SangYu
@Date  : 2019/1/9 15:25
@Desc  : 读取文件名
"""

import os


# 读取文件目录下所有文件（不包含文件夹）
def read_all_file_list(dir_path):
    """
    读取文件目录下所有文件（不包含文件夹）
    :param dir_path:文件路径
    :return:文件名（包含路径）列表
    """
    file_list = []
    for file in os.listdir(dir_path):
        file_path = os.path.join(dir_path, file)
        # 判断该路径是否是文件
        if os.path.isfile(file_path):
            file_list.append(file_path)
    return file_list


if __name__ == '__main__':
    print(read_all_file_list("..\\FileRead"))
