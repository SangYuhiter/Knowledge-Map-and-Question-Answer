# -*- coding: utf-8 -*-
'''
@File  : HanLPTest.py
@Author: SangYu
@Date  : 2018/12/27 14:56
@Desc  : 测试HanLP平台的使用
'''
from pyhanlp import *

if __name__ == "__main__":
    print(HanLP.segment("哈工大计算机学院2015年招多少人？"))
