# -*- coding: utf-8 -*-
"""
@File  : QuestionTypePredict.py
@Author: SangYu
@Date  : 2019/4/29 16:39
@Desc  : 问题类型预测
"""
import jieba
import fastText.FastText as ff
import time
import os


class QuestionTypePredict:
    """
    问题类型预测类，用于预测问题类型，规定接口可进行替换
    """
    label_to_name = None
    stop_words = None
    classifier = None

    def pre_load_jieba(self):
        """
        初始化结巴字典树
        :return:
        """
        jieba.initialize()

    def pre_load_label_name_map(self):
        """
        预加载标签名字映射
        :return:
        """
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        self.label_to_name = self.load_label_name_map("label_name_map")[0]

    def pre_load_stop_words(self):
        """
        预加载停用词
        :return:
        """
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        file_path = "stopwords.txt"
        stop_words = set()
        with open(file_path, "r", encoding="utf-8") as f_stopwords:
            for line in f_stopwords:
                stop_words.add(line.strip())
        self.stop_words = stop_words

    def pre_load_fastText_model(self):
        """
        预加载fastText模型
        :return:
        """
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        self.classifier = ff.load_model("model_w2_e24")

    def load_label_name_map(self, file_path):
        """
        加载标签名，标签映射关系
        :return:
        """
        label_to_name = {}
        name_to_label = {}
        with open(file_path, "r", encoding="utf-8") as f_label_map:
            for line in f_label_map:
                label = line.strip().split("\t")[0]
                name = line.strip().split("\t")[-1]
                label_to_name[label] = name
                name_to_label[name] = label
        return label_to_name, name_to_label

    def question_predict_by_fastText(self, question):
        """
        使用fashText对问句进行分类
        :return:
        """
        seg_line = jieba.cut(question)
        add_str = ""
        for word in seg_line:
            if word not in self.stop_words:
                add_str += word + " "
        predict = self.classifier.predict(add_str.strip())
        return self.label_to_name[predict[0][0]]


if __name__ == '__main__':
    start_time = time.time()
    qt_predict = QuestionTypePredict()
    qt_predict.pre_load_jieba()
    qt_predict.pre_load_label_name_map()
    qt_predict.pre_load_stop_words()
    qt_predict.pre_load_fastText_model()
    print("系统数据加载时间%s" % (time.time() - start_time))
    label = qt_predict.question_predict_by_fastText("我是一个男生，请老师推荐一下比较好的专业")
    print(label)
