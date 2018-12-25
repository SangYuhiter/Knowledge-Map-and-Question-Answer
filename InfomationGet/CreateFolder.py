#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File  : CreateFolder.py
@Author: SangYu
@Date  : 2018/12/21 11:02
@Desc  : 完成创建文件夹的功能
'''

import os


# 创建C9招生计划和录取分数文件夹
def create_plan_score_folder_c9():
    c9 = ["北京大学", "清华大学", "复旦大学", "上海交通大学", "浙江大学",
          "南京大学", "中国科学技术大学", "哈尔滨工业大学", "西安交通大学"]
    catalog = ["招生计划", "录取分数"]
    root_path = "Infomation/九校联盟"
    for university in c9:
        if not os.path.exists(root_path + "/" + university):
            os.makedirs(root_path + "/" + university)
            for cat in catalog:
                if not os.path.exists(root_path + "/" + university + "/" + cat):
                    os.makedirs(root_path + "/" + university + "/" + cat)
    print("文件夹创建完成！")


if __name__ == "__main__":
    create_plan_score_folder_c9()
