# -*- coding: utf-8 -*-
"""
@File  : QuestionPretreatment.py
@Author: SangYu
@Date  : 2018/12/25 15:32
@Desc  : 自然语言问句的预处理
"""
from LTP.LTPInterface import ltp_segmentor, ltp_postagger, ltp_name_entity_recognizer
from HanLP.HanLPTest import hanlp_nlp_segmentor
from TemplateLoad.QuestionTemplate import load_template_by_file
from SimilarityCalculate.SemanticSimilarity import deepintell_api_asy
from QuestionAnalysis.KeywordNormalize import time_word_normalize, district_word_normalize


# ltp对关键词的抽取与识别
# noinspection PyShadowingNames
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
# noinspection PyShadowingNames
def question_segment_hanlp(question):
    return hanlp_nlp_segmentor(question)


# 加载问题模板并返回最匹配的模板及相应的答句模板
# noinspection PyShadowingNames
def find_question_match_template(ab_question, template_sentence_type):
    main_path = "../TemplateLoad/Template"
    template_path = main_path + "/" + template_sentence_type
    fq_condition, fq_target, ts_answers, ts_questions = load_template_by_file(template_path)
    # 替换模板词
    temp_sentence = []
    for sentence in ts_questions:
        for fqc in fq_condition:
            key_en = fqc.split(" ")[0]
            key_ch = fqc.split(" ")[1]
            sentence = sentence.replace("(" + key_en + ")", key_ch).split("--")[0]
        temp_sentence.append(sentence)
    input_pairs = [{"sent1": ab_question, "sent2": sentence} for sentence in temp_sentence]
    score_list = deepintell_api_asy(input_pairs)
    score_list.sort()
    highest_index = score_list[-1][1]
    match_template_sentence = ts_questions[highest_index]
    return fq_condition, fq_target, match_template_sentence.split("--")[0], ts_answers[
        int(match_template_sentence.split("--")[1])]


# 通过分析分词结果抽象问句
# noinspection PyShadowingNames
def question_abstract(question_segment_list):
    ab_question = ""
    for item in question_segment_list:
        # 词及其词性
        word = item.split("/")[0]
        nature = item.split("/")[-1]
        # 时间词（2015年、14年）
        if nature == "t":
            ab_question += "年份"
        # 识别词为nschool
        elif nature == "nschool":
            ab_question += "学校"
        # 识别词为nmajor
        elif nature == "nmajor":
            ab_question += "专业"
        # 识别词为地名
        elif nature == "ns":
            ab_question += "省份"
        # 识别词为类别
        elif "理" in word:
            ab_question += "类别"
        elif "文" in word:
            ab_question += "类别"
            continue
        else:
            ab_question += word
    return ab_question


# 通过分析分词结果获取问题关键词信息
# noinspection PyDictCreation
def question_analysis_to_keyword(question_segment_list):
    keyword = {}
    keyword["search_year"] = ""
    keyword["search_school"] = ""
    keyword["search_major"] = ""
    keyword["search_district"] = ""
    keyword["search_classy"] = ""
    keyword["search_batch"] = ""
    keyword["search_table"] = "admission_plan"  # 默认查询招生计划
    for item in question_segment_list:
        # 词及其词性
        word = item.split("/")[0]
        nature = item.split("/")[-1]
        # 时间词（2015年、14年）
        if nature == "t":
            keyword["search_year"] = word
            continue
        # 识别词为nschool
        elif nature == "nschool":
            keyword["search_school"] = word
            continue
        # 识别词为nmajor
        elif nature == "nmajor":
            keyword["search_major"] = word
            continue
        # 识别词为地名
        elif nature == "ns":
            keyword["search_district"] = word
            continue
        # 识别词为类别
        elif "理" in word:
            keyword["search_classy"] = "理工"
            continue
        elif "文" in word:
            keyword["search_classy"] = "文史"
            continue
        # 识别为招生计划表格
        elif word.find("招生计划") != -1 or word.find("招生") != -1 or word.find("招") != -1:
            keyword["search_table"] = "admission_plan"
        elif word.find("录取分数") != -1 or word.find("分数线") != -1 or word.find("分数") != -1:
            keyword["search_table"] = "admission_score"
    # return search_table, search_year, search_school, search_major, search_district, search_classy
    return keyword


# 问题关键词规范化
def question_keyword_normalize(keyword):
    # search_table, search_year, search_school, search_major, search_district = keyword_tuple
    # 表格
    if keyword["search_table"] != "admission_plan":
        if keyword["search_major"] != "":
            keyword["search_table"] += "_major"
        else:
            keyword["search_table"] += "_pro"
    # 年份（2017年、17年）
    keyword["search_year"] = time_word_normalize(keyword["search_year"])

    # 高校（全称与简称）
    c9 = ["北京大学", "北京大学医学部", "清华大学", "复旦大学", "上海交通大学", "浙江大学",
          "南京大学", "中国科学技术大学", "哈尔滨工业大学", "西安交通大学"]
    c9_j = ["北大", "北大医学部", "清华", "复旦", "上交", "浙大",
            "南大", "中科大", "哈工大", "西交大"]
    if keyword["search_school"] in c9_j:
        keyword["search_school"] = c9[c9_j.index(keyword["search_school"])]
    # 地区
    keyword["search_district"] = district_word_normalize(keyword["search_district"])
    return keyword


if __name__ == "__main__":
    # 以该问题为例进行测试
    # question = "哈工大计算机学院2015年招多少人？"
    LTP_DATA_DIR = "../LTP/ltp_data"
    question = "哈工大2015年软件工程理科类招多少人？"
    print(question_segment_hanlp(question))
    ab_question = question_abstract(question_segment_hanlp(question))
    print(ab_question)
    # load_question_template(ab_question)
    print("end...")
