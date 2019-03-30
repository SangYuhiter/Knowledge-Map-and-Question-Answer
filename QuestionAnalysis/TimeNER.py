# -*- coding: utf-8 -*-
"""
@File  : TimeNER.py
@Author: SangYu
@Date  : 2019/3/28 13:45
@Desc  : 时间词识别
"""

from HanLP.HanLPTest import hanlp_nlp_segmentor
from datetime import datetime
import re

UTIL_CN_NUM = {
    '零': 0, '一': 1, '二': 2, '两': 2, '三': 3, '四': 4,
    '五': 5, '六': 6, '七': 7, '八': 8, '九': 9,
    '0': 0, '1': 1, '2': 2, '3': 3, '4': 4,
    '5': 5, '6': 6, '7': 7, '8': 8, '9': 9
}


def year_normalize(msg: str)->int:
    """
    年份的正则化
    :param msg: 输入时间词
    :return: 输出年份
    """
    year = re.findall(r"[0-9零一二两三四五六七八九十]{2,4}", msg)
    for item in year:
        temp = ""
        # 替换中文数字
        for char in item:
            if char in UTIL_CN_NUM:
                temp += str(UTIL_CN_NUM[char])
        # 检查数字长度
        num = re.match(r"\d+", temp)
        if num:
            # 长度为2
            if len(num.group(0)) == 2:
                return int(datetime.today().year/100)*100+int(num.group(0))
            else:
                return int(num.group(0))
        else:
            return 0


def time_extract(text: str)->list:
    """
    使用hanlp分词，提取带有时间词性的词
    :param text:含有时间词的文本
    :return:时间词列表
    """
    key_year = {"今年": 0, "去年": -1, "前年": -2}
    time_res = []
    record = ""
    for seg in hanlp_nlp_segmentor(text):
        word = seg.split("/")[0]
        nature = seg.split("/")[-1]
        # 含有key_year中的词
        if word in key_year:
            if record != "":
                time_res.append(record)
            record = str(datetime.today().year + key_year[word]) + "年"
        elif record != "":
            if nature in ["m", "t"]:
                record += word
            else:
                time_res.append(record)
                record = ""
        elif nature in ["m", "t"]:
            record = word
    if record != "":
        time_res.append(record)
    return time_res


def text_to_year(text: str)->list:
    """
    输入文本，返回文本中的年份列表
    :param text: 文本
    :return: 年份列表
    """
    if text == "":
        return []
    time_res = time_extract(text)
    return [year_normalize(msg) for msg in time_res]

if __name__ == '__main__':
    texts = ["2019年到2025年的事情", "19年的事情", "2019的事情",
             "二零一九年的事情", "一九年的事情", "二零一九的事情",
             "今年到二零二三年的事情", "去年的事情", "前年的事情"]
    for text in texts:
        year_list = text_to_year(text)
        print(year_list)
