#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File  : QuestionPretreatment.py
@Author: SangYu
@Date  : 2018/12/25 15:32
@Desc  : 自然语言问句的预处理
'''
from LTP import LTPInterface


# 读取问题输入
def read_question():
    question = input("请输入问题：")
    return question


# 分词处理
def question_segmentor(LTP_DATA_DIR, question):
    return LTPInterface.ltp_segmentor(LTP_DATA_DIR, question)


# 词性标注
def question_postagger(LTP_DATD_DIR, words):
    return LTPInterface.ltp_postagger(LTP_DATA_DIR, words)


# 命名实体识别
def question_name_entity_recognizerr(LTP_DATD_DIR, words, postags):
    return LTPInterface.ltp_name_entity_recognizer(LTP_DATA_DIR, words, postags)


if __name__ == "__main__":
    # 以该问题为例进行测试
    # question = "哈工大计算机学院2015年招多少人？"
    LTP_DATA_DIR = "../LTP/ltp_data"
    question = read_question()
    question_seg = question_segmentor(LTP_DATA_DIR, question)
    print(list(question_seg))
    question_pos = question_postagger(LTP_DATA_DIR, question_seg)
    print(list(question_pos))
    question_ner = question_name_entity_recognizerr(LTP_DATA_DIR, question_seg, question_pos)
    print(list(question_ner))
