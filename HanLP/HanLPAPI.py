# -*- coding: utf-8 -*-
"""
@File  : HanLPAPI.py
@Author: SangYu
@Date  : 2018/12/27 14:56
@Desc  : HanLP平台的API
"""
from pyhanlp import *
from Log.Logger import MyLog


# 分词（有词性标注）
def hanlp_nlp_segmentor(sentence):
    nlp_tokenizer = JClass("com.hankcs.hanlp.tokenizer.NLPTokenizer")
    return str(nlp_tokenizer.analyze(sentence)).split(" ")


# 分词（无词性标注）
def hanlp_nlp_segmentor_without_nature(sentence):
    nlp_tokenizer = JClass("com.hankcs.hanlp.tokenizer.NLPTokenizer")
    word_list = str(nlp_tokenizer.analyze(sentence)).split(" ")
    return [word.split("/")[0] for word in word_list]


if __name__ == "__main__":
    mylogger = MyLog(logger=__name__).getlog()
    mylogger.info("start...")
    print(type(hanlp_nlp_segmentor("2015年哈工大软件工程在河南招多少人？")))
    print(hanlp_nlp_segmentor("一五年哈工大软件工程在河南招多少人？"))
    mylogger.info("end...")
