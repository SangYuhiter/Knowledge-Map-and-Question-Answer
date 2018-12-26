#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
@File  : XFYunWebAPI.py
@Author: SangYu
@Date  : 2018/12/26 11:03
@Desc  : 讯飞云网络接口API
'''
# 使用网络接口访问服务
import time
import urllib.request
import urllib.parse
import json
import hashlib
import base64


# 讯飞云ltp平台
def ltp_service(func, TEXT, x_appid, api_key):
    # 接口地址
    url = "http://ltpapi.xfyun.cn/v1/" + func
    body = urllib.parse.urlencode({'text': TEXT}).encode('utf-8')
    param = {"type": "dependent"}
    x_param = base64.b64encode(json.dumps(param).replace(' ', '').encode('utf-8'))
    x_time = str(int(time.time()))
    x_checksum = hashlib.md5(api_key.encode('utf-8') + str(x_time).encode('utf-8') + x_param).hexdigest()
    x_header = {'X-Appid': x_appid,
                'X-CurTime': x_time,
                'X-Param': x_param,
                'X-CheckSum': x_checksum}
    req = urllib.request.Request(url, body, x_header)
    result = urllib.request.urlopen(req)
    result_json = json.loads(result.read())
    print(result_json)
    print(result_json["data"])
    return result_json


if __name__ == "__main__":
    # 讯飞云开放功能模块
    # 中文分词(cws)、词性标注(pos)、依存句法分析(dp)、命名实体识别(ner)、
    # 语义角色标注(srl)、语义依存 (依存树) 分析(sdp)、语义依存 (依存图) 分析(sdgp)
    func = ["cws", "pos", "dp", "ner", "srl", "sdp", "sdgp"]
    # 返回节点
    data = ["word", "pos", "dp", "ner", "srl", "sdp", "sdgp"]
    # 语言文本
    TEXT = "汉皇重色思倾国，御宇多年求不得。杨家有女初长成，养在深闺人未识。天生丽质难自弃，一朝选在君王侧。"
    # 开放平台应用ID
    x_appid = "5c22dc4a"
    # 开放平台应用接口秘钥
    api_key = "83430b181393671a76842e526b304ce1"
    ltp_service(func[0], TEXT, x_appid, api_key)
    # for fun in func:
    #     ltp_service(fun, TEXT, x_appid, api_key)
