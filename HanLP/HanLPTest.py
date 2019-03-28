# -*- coding: utf-8 -*-
"""
@File  : HanLPTest.pysou
@Author: SangYu
@Date  : 2018/12/27 14:56
@Desc  : 测试HanLP平台的使用
"""
from pyhanlp import *
import sys
from Log.Logger import MyLog
import datetime
import json
import requests
import time


# 分词
def hanlp_nlp_segmentor(sentence):
    nlp_tokenizer = JClass("com.hankcs.hanlp.tokenizer.NLPTokenizer")
    return str(nlp_tokenizer.analyze(sentence)).split(" ")
    # return nlp_tokenizer.analyze(sentence).translateLabels()


# 外部接口
def hanlp_nlp_segmentor_api(sentence):
    send = {
        "packageName": "tokenizer.Tokenizer",
        "methodName": "segment",
        "params": [{
            "key": "string",
            "value": sentence
        }]
    }
    # print(send)
    src = json.dumps(send)
    url = "http://192.168.100.201:8888/App/webAsync"
    headers = {'content-type': 'application/json'}
    r = requests.post(url=url, data=src, headers=headers, timeout=7)
    return r


if __name__ == "__main__":
    mylogger = MyLog(logger=__name__).getlog()
    mylogger.info("start...")
    # print(type(hanlp_nlp_segmentor("2015年哈工大软件工程在河南招多少人？")))
    # print(hanlp_nlp_segmentor("2015年哈工大软件工程在河南招多少人？"))
    # print(hanlp_nlp_segmentor("战争动员学的学院"))
    # print(hanlp_nlp_segmentor("内蒙古"))
    print(hanlp_nlp_segmentor("我是哈尔滨工业大学(威海)的软件工程的一批次理工类考生"))
    # nowTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # print(nowTime)

    # senntence = "asdfasdfasdhttps://blog.csdn.net/a13278883533/article/details/79651417为欧文啊实打实的发"
    # time_start = time.time()
    # result = hanlp_nlp_segmentor_api(senntence)
    # time_end = time.time()
    # print("api:%s ms" % ((time_end-time_start)*1000))
    # result.encoding = result.apparent_encoding
    # print(result.text)

    # time_start = time.time()
    # result = hanlp_nlp_segmentor(senntence)
    # time_end = time.time()
    # print("local:%s ms" % ((time_end - time_start)*1000))
    # print(result)

    sentences = ["2015年哈工大软件工程在河南招多少人？", "2015年复旦大学机械工程录取分数是多少？"]
    # result = hanlp_nlp_segmentor(sentences)
    # print(result)
    # print(str(sentences))
    # result = hanlp_nlp_segmentor_api(str(sentences))
    # result.encoding = result.apparent_encoding
    # print(result.text)

    mylogger.info("end...")
