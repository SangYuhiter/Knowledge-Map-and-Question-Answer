# -*- coding: utf-8 -*-
'''
@File  : HanLPTest.py
@Author: SangYu
@Date  : 2018/12/27 14:56
@Desc  : 测试HanLP平台的使用
'''
from pyhanlp import *
import logging

# 日志格式设置
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
DATE_FORMAT = "%m/%d/%Y %H:%M:%S %p"
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT, datefmt=DATE_FORMAT)



# 分词
def hanlp_nlp_segmentor(sentence):
    NLPTokenizer = JClass("com.hankcs.hanlp.tokenizer.NLPTokenizer")
    return str(NLPTokenizer.analyze(sentence)).split(" ")
    # return NLPTokenizer.analyze(sentence).translateLabels()


if __name__ == "__main__":
    logger = logging.getLogger(__name__)
    logger.info("start...")
    # print(type(hanlp_nlp_segmentor("2015年哈工大软件工程在河南招多少人？")))
    # print(hanlp_nlp_segmentor("2015年哈工大软件工程在河南招多少人？"))
    # print(hanlp_nlp_segmentor("战争动员学的学院"))
    # print(hanlp_nlp_segmentor("内蒙古"))
    logger.debug("*************")
    logger.info("*************")
    logger.warning("*************")
    logger.error("*************")
    logger.critical("*************")
    logger.info("end...")