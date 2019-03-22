# -*- coding: utf-8 -*-
"""
@File  : KeywordNormalize.py
@Author: SangYu
@Date  : 2019/3/18 10:35
@Desc  : 关键词正则化
"""
from Log.Logger import MyLog
import json
import requests


# input: string
# output:
# N/A 表示非时间
# 时间点(timestamp)
# 时间区间(timespan)timespan 表示时间点组成的时间区间结果，格式为[timestamp,timestamp]表示时间区间的起始和结束时间
# 时间量(timedelta)
# 格式为[timedelta,*]表示时间量, 如有多个时间量时则会全部列举出来
# json:
# 生日快乐
# {"N/A": "no time pattern could be extracted."}
# 二〇一七年十一月十九日
# {"timestamp": "2017-11-19 00:00:00", "type": "timestamp"}
# 从8点到10点
# {"type": "timespan", "timespan": ["2017-12-18 08:00:00", "2017-12-18 10:00:00"]}
# 二十个小时
# {"type": "timedelta", "timedelta": ["0 days, 20:00:00"]}
# 三天
# {"type": "timedelta", "timedelta": ["3 days, 0:00:00"]}
# 过去的三个月
# {"type": "timedelta", "timedelta": ["90 days, 0:00:00"]}
# 大概四到五天
# {"type": "timedelta", "timedelta": ["4 days, 0:00:00", "5 days, 0:00:00"]}
# 本程序也同时支持农历和节日的识别, 如:
# 今年农历四月初五
# {"timestamp": "2017-04-30 00:00:00", "type": "timestamp"}
# 明年春节到元宵节
# {"type": "timespan", "timespan": ["2018-02-16 00:00:00", "2018-03-02 00:00:00"]}
# 时间词正则化，返回20xx(年)
# noinspection PyDictCreation
def time_word_normalize(time_word):
    src = time_word
    # 外部访问url
    url_web = 'http://api.deepintell.net/timeanlz'
    # 内网访问
    # url = "http://192.168.100.202:20002"
    param = {}
    param['query'] = src
    # 外部访问头
    headers_web = {'X-Token': 'hqcK70wBTd2vqsI18JgUFUQXbbCp5JdL', 'Content-type': 'application/json',
                   'Accept': 'application/json'}
    # headers = {'content-type': 'application/json', 'Accept': 'application/json'}
    r = requests.post(url=url_web, data=json.dumps(param), headers=headers_web, timeout=3)
    # 两个接口返回参数不同，注意区别
    # time_word_dict = json.loads(r.json())
    time_word_dict = r.json()
    year = ""
    if "timestamp" in time_word_dict:
        year = time_word_dict["timestamp"][:4]
    return year


# 返回结果为json字典列表(如下)：当有多个地理信息出现时识别出多个信息, 各信息以列表的形式返回
# [{'country': '中国', 'province': ' ', 'city': '北京', 'zone': '', 'town': '',
# 'stamp': {'start': 3, 'end': 5, 'words': '北京'}},
# {'country': '中国', 'province': ' ', 'city': '上海', 'zone': '', 'town': '',
# 'stamp': {'start': 6, 'end': 8, 'words': '上海'}}]
# keys:
# "country": 国家名
# "province": 省名
# "city": 市名
# "zone": 区 / 镇名
# "town": 乡名
# "stamp": 地理词在句子中的位置
# "start": 起始位置(不包含)
# "end": 终止位置(不包含)
# "words": 识别出的地理词
# 例如:
# 输入: 我要去金华买火腿, 我该怎么走?
# 返回结果: 返回信息包括, 国家, 省, 市, 区, 乡, 地理词汇在文中的起点和终点
# [{'country': '中国', 'province': '浙江', 'city': '金华', 'zone': '', 'town': '',
# 'stamp': {'start': 3, 'end': 5, 'words': '金华'}}]
# 地点词正则化
# noinspection PyDictCreation
def district_word_normalize(district_word):
    src = district_word
    # 外部访问
    url_web = 'http://api.deepintell.net/locanlz'
    # 内网访问
    # url = "http://192.168.100.202:20001"
    param = {}
    param['query'] = src
    # 在http://deepintell.net上注册用户获取api密钥
    headers_web = {'X-Token': 'hqcK70wBTd2vqsI18JgUFUQXbbCp5JdL', 'Content-type': 'application/json',
                   'Accept': 'application/json'}
    # headers = {'content-type': 'application/json', 'Accept': 'application/json'}
    r = requests.post(url=url_web, data=json.dumps(param), headers=headers_web, timeout=3)
    # print(r.json())
    district = ""
    if len(r.json()) != 0:
        district_word_dict = r.json()[0]
        # print(district_word_dict)
        if district_word_dict["province"] == " ":
            district = district_word_dict["city"]
        else:
            district = district_word_dict["province"]
    return district


if __name__ == '__main__':
    main_logger = MyLog(logger=__name__).getlog()
    main_logger.info("start...")
    test_time_word = "我要去金华买火腿, 我该怎么走?"
    test_district_word = "今年农历四月初五"
    # print(time_word_normalize(test_time_word))
    r_district = district_word_normalize(test_district_word)
    print(r_district)
    main_logger.info("end...")
