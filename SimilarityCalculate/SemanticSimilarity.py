# -*- coding: utf-8 -*-
"""
@File  : SemanticSimilarity.py
@Author: SangYu
@Date  : 2019/3/16 15:02
@Desc  : 语义相似度计算
"""
from Log.Logger import MyLog
import sys
import json
import asyncio
import aiohttp
import requests


# 深智语义相似度计算api,输入：句子对,对序号，分数列表
async def deepintell_api(input_pair, i_pair, score_list):
    async with aiohttp.ClientSession()as session:
        src = json.dumps(input_pair)
        # 外部访问
        url_web = "http://test.deepintell.net/api"
        url = "http://192.168.100.202:20031/api"
        headers = {'content-type': 'application/json'}
        async with session.post(url=url_web, data=src, headers=headers, timeout=10) as response:
            result = await response.json()
            result_json = json.loads(result)
            # print("result:"+result["final_score"])
            score_list.append([result_json["final_score"], i_pair])


# 异步访问API接口，获取匹配结果，输入：句子对
def deepintell_api_asy(input_pairs):
    score_list = []
    oldloop = asyncio.get_event_loop()
    run_event_loop(input_pairs,score_list)
    asyncio.set_event_loop(oldloop)
    return score_list

def run_event_loop(input_pairs,score_list):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    tasks = [deepintell_api(input_pairs[i_pair], i_pair, score_list) for i_pair in range(len(input_pairs))]
    loop.run_until_complete(asyncio.wait(tasks))
    loop.close()



if __name__ == '__main__':
    mylogger = MyLog(logger=__name__).getlog()
    mylogger.info("start...")
    input_pair = {"sent1": "我是哈工大的学生", "sent2": "我是哈工程的学生"}
    src = json.dumps(input_pair)
    # 外部访问
    url_web = "http://test.deepintell.net/api"
    url = "http://192.168.100.202:20031/api"
    headers = {'content-type': 'application/json'}
    r = requests.post(url=url, data=src, headers=headers, timeout=7)
    result = r.json()
    print(result)
    mylogger.info("end...")

