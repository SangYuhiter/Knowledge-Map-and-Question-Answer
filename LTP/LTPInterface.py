# -*- coding: utf-8 -*-
"""
@File  : LTPInterface.py
@Author: SangYu
@Date  : 2018/12/25 15:39
@Desc  : 哈工大LTP平台自然语言处理工具接口
"""
# 使用pyltp完成自然语言处理
import os
from pyltp import Segmentor  # 分句
from pyltp import SentenceSplitter  # 分词
from pyltp import Postagger  # 词性标注
from pyltp import NamedEntityRecognizer  # 命名实体识别
from pyltp import Parser  # 依存句法分析
from pyltp import SementicRoleLabeller  # 语义角色标注


# 分句
# noinspection PyShadowingNames,PyArgumentList
def ltp_sentence_split(sentences):
    return SentenceSplitter.split(sentences)  # 分句


# 分词
# noinspection PyShadowingNames,PyArgumentList,PyPep8Naming
def ltp_segmentor(LTP_DATA_DIR, sentence):
    # 分词模型路径，模型名称为`cws.model`
    cws_model_path = os.path.join(LTP_DATA_DIR, "cws.model")
    segmentor = Segmentor()  # 初始化实例
    # segmentor.load(cws_model_path)  # 加载模型
    segmentor.load_with_lexicon(cws_model_path, "ltp_data/dict/school")
    words = segmentor.segment(sentence)  # 分词
    segmentor.release()  # 释放模型
    return words


# 词性标注
# noinspection PyShadowingNames,PyArgumentList,PyPep8Naming
def ltp_postagger(LTP_DATA_DIR, words):
    # 词性标注模型路径，模型名称为`pos.model`
    pos_model_path = os.path.join(LTP_DATA_DIR, 'pos.model')
    postagger = Postagger()  # 初始化实例
    postagger.load(pos_model_path)  # 加载模型
    postags = postagger.postag(words)  # 词性标注
    postagger.release()  # 释放模型
    return postags


# 命名实体识别
# noinspection PyShadowingNames,PyArgumentList,PyPep8Naming
def ltp_name_entity_recognizer(LTP_DATA_DIR, words, postags):
    # 命名实体识别模型路径，模型名称为`ner.model`
    ner_model_path = os.path.join(LTP_DATA_DIR, 'ner.model')
    recognizer = NamedEntityRecognizer()  # 初始化实例
    recognizer.load(ner_model_path)  # 加载模型
    netags = recognizer.recognize(words, postags)  # 命名实体识别
    recognizer.release()  # 释放模型
    return netags


# 依存句法分析
# noinspection PyShadowingNames,PyArgumentList,PyPep8Naming
def ltp_parser(LTP_DATA_DIR, words, postags):
    # 依存句法分析模型路径，模型名称为`parser.model`
    par_model_path = os.path.join(LTP_DATA_DIR, 'parser.model')
    parser = Parser()  # 初始化实例
    parser.load(par_model_path)  # 加载模型
    arcs = parser.parse(words, postags)  # 句法分析
    parser.release()  # 释放模型
    return arcs


# 语义角色标注
# noinspection PyShadowingNames,PyArgumentList,PyPep8Naming
def ltp_sementic_role_labeller(LTP_DATA_DIR, words, postags, arcs):
    # 语义角色标注模型目录路径，模型目录为`srl`。注意该模型路径是一个目录，而不是一个文件。
    # windos下开发使用pisrl_win.model模型
    srl_model_path = os.path.join(LTP_DATA_DIR, 'srl/pisrl_win.model')
    labeller = SementicRoleLabeller()  # 初始化实例
    labeller.load(srl_model_path)  # 加载模型
    # arcs 使用依存句法分析的结果
    roles = labeller.label(words, postags, arcs)  # 语义角色标注
    labeller.release()  # 释放模型
    return roles


if __name__ == "__main__":
    # pyltp功能测试
    LTP_DATA_DIR = "ltp_data"  # ltp_data模型目录位置
    # 分句测试
    sentence = "元芳你怎么看？扒窗户上看呗！"
    sents = ltp_sentence_split(sentence)
    print("分句测试")
    print("返回类型：", sents)
    print("列表化：", list(sents))
    # 分词测试
    test_sentence = "哈尔滨工业大学计算机学院的学生人数？"
    words = ltp_segmentor(LTP_DATA_DIR, test_sentence)
    print("分词测试")
    print("返回类型：", words)
    print("列表化：", list(words))
    # 词性标注
    postags = ltp_postagger(LTP_DATA_DIR, words)
    print("词性标注测试")
    print("返回类型：", postags)
    print("列表化：", list(postags))
    netags = ltp_name_entity_recognizer(LTP_DATA_DIR, words, postags)
    print("命名实体识别测试")
    print("返回类型：", netags)
    print("列表化：", list(netags))
    arcs = ltp_parser(LTP_DATA_DIR, words, postags)
    # print("依存句法分析测试")
    # print("返回类型：", netags)
    # print("\t".join("%d:%s" % (arc.head, arc.relation) for arc in arcs))
    # roles = ltp_sementic_role_labeller(LTP_DATA_DIR, words, postags, arcs)
    # print("依存句法分析测试")
    # print("返回类型：", roles)
    # for role in roles:
    #     print(role.index, "".join(
    #         ["%s:(%d,%d)" % (arg.name, arg.range.start, arg.range.end) for arg in role.arguments]))
