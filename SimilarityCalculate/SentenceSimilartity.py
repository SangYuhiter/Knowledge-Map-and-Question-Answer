# -*- coding: utf-8 -*-
"""
@File  : SentenceSimilartity.py
@Author: SangYu
@Date  : 2019/3/30 12:10
@Desc  : 
"""
import distance


def edit_distance(sen1: str, sen2s: list)->list:
    """
    使用编辑距离衡量句子相似度
    :param sen1: 查询句
    :param sen2s: 备选句子组
    :return: 最相似的句子
    """
    result = []
    for i_sen in range(len(sen2s)):
        result.append((distance.nlevenshtein(sen1, sen2s[i_sen]), i_sen, sen2s[i_sen]))
    return sorted(result)


if __name__ == '__main__':
    # sen1 = "我是学生"
    # sentences = ["我是哈工程的学生", "我是哈工大的大学生"]
    # result = edit_distance(sen1, sentences)
    test1 = "我是学生"
    test2 = "我是教师"
    # print(distance.nlevenshtein(test1, test2, 2))
    # print(result)
