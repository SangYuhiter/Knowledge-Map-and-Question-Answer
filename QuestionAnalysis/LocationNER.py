# -*- coding: utf-8 -*-
"""
@File  : LocationNER.py
@Author: SangYu
@Date  : 2019/3/28 20:38
@Desc  : 地点词识别
"""
import json

# 加载行政区划json文件
def load_location():
    path = "Area/level4-full.json"
    with open(path,"r",encoding="utf-8") as load_f:
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


def text_to_location(text: str)->str:
    """
    输入文本，返回文本中的地点列表
    :param text: 文本
    :return: 地点列表
    """
    pro_dict, city_dict = load_location()
    city_id = 0
    for key in city_dict:
        if text in city_dict[key]:
            city_id = key
            print(city_id)
            break
    if city_id!=0:
        print(city_id[:2])
        return pro_dict[city_id[:2]]
    else:
        return "无查询结果"

if __name__ == '__main__':
    # load_location()
    print(text_to_location("石家庄"))