# -*- coding: utf-8 -*-
"""
@File  : LocationNER.py
@Author: SangYu
@Date  : 2019/3/28 20:38
@Desc  : 地点词识别
"""
import json
from HanLP.HanLPTest import hanlp_nlp_segmentor
import os


# 加载行政区划json文件
def load_location():
    os.chdir(os.path.split(os.path.realpath(__file__))[0])
    path = "Area/level4-full.json"
    with open(path, "r", encoding="utf-8") as load_f:
        load_dict = json.load(load_f)
    # 省一级别
    pro_dict = {}
    for pro_json in load_dict["children"]:
        pro_dict[pro_json["divisionId"][:2]] = pro_json["divisionName"]
    # for key in pro_dict:
    #     print(key+pro_dict[key])
    # 市一级别
    city_dict = {}
    for pro_json in load_dict["children"]:
        for city_json in pro_json["children"]:
            city_dict[city_json["divisionId"]] = city_json["divisionName"]
    # for key in city_dict:
    #     print(key+city_dict[key])
    return pro_dict, city_dict


def province_normalize(msg: str) -> str:
    """
    省份的正则化
    :param msg: 输入地点词
    :return: 输出省份
    """
    sub_word = ["省", "市"]
    for sw in sub_word:
        msg = msg.replace(sw, "")
    pro_dict, city_dict = load_location()
    # 省份中能找到
    for key in pro_dict:
        if msg in pro_dict[key]:
            return pro_dict[key]
    # 城市中能找到
    city_id = 0
    for key in city_dict:
        if msg in city_dict[key]:
            city_id = key
            break
    if city_id != 0:
        return pro_dict[city_id[:2]]
    else:
        return ""


def location_extract(text: str) -> list:
    """
    使用hanlp分词，提取带有地点词性的词
    :param text:含有地点词的文本
    :return:时间词列表
    """
    location_res = []
    # print("分词结果"+str(hanlp_nlp_segmentor(text)))
    for seg in hanlp_nlp_segmentor(text):
        word = seg.split("/")[0]
        nature = seg.split("/")[-1]
        # 含有key_year中的词
        if nature in ["ns", "nr"]:
            location_res.append(word)
    return location_res


def text_to_location(text: str) -> list:
    """
    输入文本，返回文本中的地点列表
    :param text: 文本
    :return: 地点列表
    """
    location_res = location_extract(text)
    # print("地点词识别结果"+str(location_res))
    return [province_normalize(msg) for msg in location_res]


if __name__ == '__main__':
    # load_location()
    texts = ["黑龙江省哈尔滨市", "黑龙江省", "哈尔滨市",
             "黑龙江哈尔滨", "黑龙江", "哈尔滨"]
    for text in texts:
        location_list = text_to_location(text)
        print(location_list)
