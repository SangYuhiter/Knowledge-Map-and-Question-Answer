#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File  : CreateFolder.py
@Author: SangYu
@Date  : 2018/12/21 11:02
@Desc  : 完成创建文件夹的功能（工程项目开始时的操作）
'''
import os
import sys
from Log.Logger import MyLog


# 创建C9（包括其可能存在的医学部）招生计划和录取分数文件夹
def create_plan_score_folder_c9():
    mylogger = MyLog(logger=sys._getframe().f_code.co_name).getlog()
    # C9及其医学部
    c9 = ["北京大学", "清华大学", "复旦大学", "上海交通大学", "浙江大学",
          "南京大学", "中国科学技术大学", "哈尔滨工业大学", "西安交通大学",
          "北京大学医学部", "上海交通大学医学部", "复旦大学上海医学部"]
    catalog = ["招生计划", "录取分数"]
    root_path = "Information/九校联盟"
    for university in c9:
        mylogger.info("创建%s的文件夹" % university)
        if not os.path.exists(root_path + "/" + university):
            os.makedirs(root_path + "/" + university)
            for cat in catalog:
                if not os.path.exists(root_path + "/" + university + "/" + cat):
                    os.makedirs(root_path + "/" + university + "/" + cat)
                    # 创建source文件夹（存储网络爬取的原始数据）
                    if not os.path.exists(root_path + "/" + university + "/" + cat + "/source"):
                        os.makedirs(root_path + "/" + university + "/" + cat + "/source")
        mylogger.info("%s的文件夹创建完成！" % university)


if __name__ == "__main__":
    mylogger = MyLog(logger=__name__).getlog()
    mylogger.info("start...")
    create_plan_score_folder_c9()
    mylogger.info("end...")
