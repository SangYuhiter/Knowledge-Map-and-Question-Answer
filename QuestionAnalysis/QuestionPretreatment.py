#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File  : QuestionPretreatment.py
@Author: SangYu
@Date  : 2018/12/25 15:32
@Desc  : 自然语言问句的预处理
'''
from LTP.LTPInterface import ltp_segmentor, ltp_postagger, ltp_name_entity_recognizer
from HanLP.HanLPTest import hanlp_nlp_segmentor


# ltp对关键词的抽取与识别
def question_to_keyword_ltp(question):
    words = list(ltp_segmentor(LTP_DATA_DIR, question))
    postags = list(ltp_postagger(LTP_DATA_DIR, words))
    nertags = list(ltp_name_entity_recognizer(LTP_DATA_DIR, words, postags))
    # 先考虑命名实体的存在,组合分散的命名实体
    ner_dict = []
    for i_ner in range(len(nertags)):
        if nertags[i_ner] == "O":
            continue
        elif nertags[i_ner].find("S") != -1:
            ner_dict.append(words[i_ner] + "-" + nertags[i_ner].split("-")[-1])
    i_ner = 0
    while i_ner < len(nertags):
        if nertags[i_ner].find("B") != -1:
            end_ner = nertags.index("E-" + nertags[i_ner].split("-")[-1])
            ner_words = words[i_ner]
            for i in range(i_ner + 1, end_ner + 1):
                ner_words += words[i]
            ner_words += "-" + nertags[i_ner].split("-")[-1]
            ner_dict.append(ner_words)
            i_ner = end_ner + 1
        else:
            i_ner += 1

    search_year = ""
    search_school = ""
    search_district = ""
    # 输出查询的年份
    if "nt" in postags:
        search_year = words[postags.index("nt")]

    # 输出查询的学校,地区
    # 先查看命名实体内
    search_school = ""
    search_district = ""
    if len(ner_dict) != 0:
        for item in ner_dict:
            if item.find("Ni") != -1:
                search_school = item.split("-")[0]
            if item.find("Ns") != -1:
                search_district = item.split("-")[0]
    # 再查看命名缩写
    if search_school == "" and "j" in postags:
        search_school = words[postags.index("j")]
        print(search_school)
    if search_district == "" and "ns" in postags:
        search_district = words[postags.index("ns")]
    return search_year, search_school, search_district


# 使用hanlp平台对问答界面传入的问句进行分词预处理，返回分词及词性列表
def question_segment_hanlp(question):
    return hanlp_nlp_segmentor(question)


# 通过分析分词结果获取问题关键词信息
def question_analysis_to_keyword(question_segment_list):
    search_year = ""
    search_school = ""
    search_major = ""
    search_district = ""
    search_table = "admission_plan"  # 默认查询招生计划
    for item in question_segment_list:
        # 词及其词性
        word = item.split("/")[0]
        nature = item.split("/")[-1]
        # 时间词（2015年、14年）
        if nature == "t":
            search_year = word
        # 识别词为nschool
        elif nature == "nschool":
            search_school = word
        # 识别词为nmajor
        elif nature == "nmajor":
            search_major = word
        # 识别词为地名
        elif nature == "ns":
            search_district = word
        # 识别为招生计划表格
        elif word.find("招生计划") != -1 or word.find("招生") != -1 or word.find("招") != -1:
            search_table = "admission_plan"
        elif word.find("录取分数") != -1 or word.find("分数线") != -1 or word.find("分数") != -1:
            search_table = "admission_score"
    return search_table, search_year, search_school, search_major, search_district


# 问题关键词规范化
def question_keyword_normalize(keyword_tuple):
    search_table, search_year, search_school, search_major, search_district = keyword_tuple
    # 表格
    if search_table != "admission_plan":
        if search_major != "":
            search_table += "_major"
        else:
            search_table += "_pro"
    # 年份（2017年、17年）
    # 去除"年"字
    if search_year.find("年") != -1:
        search_year = search_year.replace("年", "")

    # 高校（全称与简称）
    c9 = ["北京大学", "北京大学医学部", "清华大学", "复旦大学", "上海交通大学", "浙江大学",
          "南京大学", "中国科学技术大学", "哈尔滨工业大学", "西安交通大学"]
    c9_j = ["北大", "北大医学部", "清华", "复旦", "上交", "浙大",
            "南大", "中科大", "哈工大", "西交大"]
    if search_school in c9_j:
        search_school = c9[c9_j.index(search_school)]

    # 地区
    if search_district.find("省") != -1:
        search_district = search_district.replace("省", "")
    return search_table, search_year, search_school, search_major, search_district


if __name__ == "__main__":
    # 以该问题为例进行测试
    # question = "哈工大计算机学院2015年招多少人？"
    LTP_DATA_DIR = "../LTP/ltp_data"
    print("end...")
