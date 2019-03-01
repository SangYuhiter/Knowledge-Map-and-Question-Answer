# -*- coding: utf-8 -*-
'''
@File  : QASystem.py
@Author: SangYu
@Date  : 2018/12/28 13:42
@Desc  : 问答系统界面
'''
import sys
from PyQt5.QtWidgets import (QMainWindow, QApplication, QAction,
                             QLabel, QLineEdit, QWidget, QTextEdit, QComboBox, QHBoxLayout, QVBoxLayout,
                             QMessageBox, QDesktopWidget, QPushButton)
from PyQt5.QtGui import QIcon

from LTP.LTPInterface import ltp_segmentor, ltp_postagger, ltp_name_entity_recognizer
from InformationGet.MysqlOperation import connect_mysql_with_db
from pypinyin import lazy_pinyin

from HanLP.HanLPTest import hanlp_nlp_segmentor

from InformationGet import MysqlOperation

LTP_DATA_DIR = "../LTP/ltp_data"


# 主界面
class QASystemMainWindow(QMainWindow):
    # 构造方法
    def __init__(self):
        super().__init__()
        self.initUI()

    # GUI创建
    def initUI(self):
        # 创建菜单栏
        self.create_menu()
        # 创建工具栏
        self.create_tool()
        # 创建状态栏
        self.statusBar()

        # 问答组件
        self.nowwid = QA_widgets()
        self.setCentralWidget(self.nowwid)

        # 窗口信息设置
        self.setGeometry(300, 300, 800, 800)
        self.center()
        self.setWindowTitle("自动问答系统")
        self.setWindowIcon(QIcon("images/cat.jpg"))
        self.show()

    # 窗口居中
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    # 创建菜单
    def create_menu(self):
        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu('File')
        exit_menu = menu_bar.addMenu('Exit')

        # 查看数据库
        mysql_act = QAction(QIcon('images/mysql.png'), 'MySQL', self)
        mysql_act.setShortcut('Ctrl+M')
        mysql_act.setStatusTip('MySQL Database')
        mysql_act.triggered.connect(self.turn_page_mysql)
        # 退出程序
        exit_act = QAction(QIcon('images/quit.png'), 'Exit', self)
        exit_act.setShortcut('Ctrl+Q')
        exit_act.setStatusTip('Exit application')
        exit_act.triggered.connect(self.close)

        exit_menu.addAction(exit_act)
        file_menu.addAction(mysql_act)

    # 创建工具栏
    def create_tool(self):
        exitAct = QAction(QIcon('images/quit.png'), 'Exit', self)
        exitAct.setShortcut('Ctrl+Q')
        exitAct.setStatusTip('Exit application')
        exitAct.triggered.connect(self.close)

        toolbar = self.addToolBar('Exit')
        toolbar.addAction(exitAct)

    def turn_page_mysql(self):
        self.MySQL_wid = MySQL_widgets()
        self.MySQL_wid.show()

    # 关闭窗口事件
    def closeEvent(self, event):
        reply = QMessageBox.question(self, '消息',
                                     "关闭系统吗？", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()


# QA部分控件
class QA_widgets(QWidget):
    # 构造方法
    def __init__(self):
        super().__init__()
        self.initUI()

    # GUI创建
    def initUI(self):
        # 保存ltp处理结果
        self.ltp_result_dict = {}
        self.create_QA_widgets()

    # 创建问答控件
    def create_QA_widgets(self):
        question = QLabel('Question')
        answer = QLabel('Answer')

        # 按钮
        self.clear_btn = QPushButton('清空')
        self.clear_btn.clicked.connect(self.clear_button)
        self.seg_btn = QPushButton('ltp分词')
        self.seg_btn.setCheckable(True)
        self.seg_btn.clicked[bool].connect(self.ltp_op)
        self.pos_btn = QPushButton('ltp词性标注')
        self.pos_btn.setCheckable(True)
        self.pos_btn.clicked[bool].connect(self.ltp_op)
        self.ner_btn = QPushButton('ltp命名实体识别')
        self.ner_btn.setCheckable(True)
        self.ner_btn.clicked[bool].connect(self.ltp_op)
        self.qa_btn = QPushButton('回答提问')
        self.qa_btn.clicked.connect(self.question_answer)

        # 编辑文本框
        self.question_edit = QLineEdit(self)
        self.answer_edit = QTextEdit(self)

        # 布局方式
        question_hbox = QHBoxLayout()
        question_hbox.addWidget(question)
        # question_hbox.addStretch(1)
        question_hbox.addWidget(self.question_edit)

        answer_hbox = QHBoxLayout()
        answer_hbox.addWidget(answer)
        # answer_hbox.addStretch(1)
        answer_hbox.addWidget(self.answer_edit)

        button_box = QHBoxLayout()
        button_box.addStretch(1)
        button_box.addWidget(self.clear_btn)
        button_box.addWidget(self.seg_btn)
        button_box.addWidget(self.pos_btn)
        button_box.addWidget(self.ner_btn)
        button_box.addWidget(self.qa_btn)

        vbox = QVBoxLayout()
        # vbox.addStretch(1)
        vbox.addLayout(question_hbox)
        # vbox.addStretch(1)
        vbox.addLayout(answer_hbox)
        # vbox.addStretch(1)
        vbox.addLayout(button_box)
        # vbox.addStretch(1)

        self.setLayout(vbox)

    # ltp操作（分词、词性标注、命名实体识别）
    def ltp_op(self, pressed):
        source = self.sender()
        if pressed:
            flag = True
        else:
            flag = False
        sentence = self.question_edit.text()
        words = ltp_segmentor(LTP_DATA_DIR, sentence)
        postags = ltp_postagger(LTP_DATA_DIR, words)
        nertags = ltp_name_entity_recognizer(LTP_DATA_DIR, words, postags)
        if source.text() == "分词":
            if pressed:
                self.ltp_result_dict["seg"] = list(words)
            else:
                if self.ltp_result_dict.__len__() != 0:
                    self.ltp_result_dict.pop("seg")
        elif source.text() == "词性标注":
            if pressed:
                self.ltp_result_dict["pos"] = list(postags)
            else:
                if self.ltp_result_dict.__len__() != 0:
                    self.ltp_result_dict.pop("pos")
        else:
            if pressed:
                self.ltp_result_dict["ner"] = list(nertags)
            else:
                if self.ltp_result_dict.__len__() != 0:
                    self.ltp_result_dict.pop("ner")
        dict_list_str = ""
        for key, value in self.ltp_result_dict.items():
            dict_list_str += '{k}:{v}'.format(k=key, v=value) + "\n"
        self.answer_edit.setText(dict_list_str)

    # 回答提出的问题
    def question_answer(self):
        self.answer_edit.clear()
        sentence = self.question_edit.text()
        # ltp方法
        # words = list(ltp_segmentor(LTP_DATA_DIR, sentence))
        # postags = list(ltp_postagger(LTP_DATA_DIR, words))
        # nertags = list(ltp_name_entity_recognizer(LTP_DATA_DIR, words, postags))
        # # 先考虑命名实体的存在,组合分散的命名实体
        # ner_dict = []
        # for i_ner in range(len(nertags)):
        #     if nertags[i_ner] == "O":
        #         continue
        #     elif nertags[i_ner].find("S") != -1:
        #         ner_dict.append(words[i_ner]+"-"+nertags[i_ner].split("-")[-1])
        # i_ner = 0
        # while i_ner < len(nertags):
        #     if nertags[i_ner].find("B") != -1:
        #         end_ner = nertags.index("E-"+nertags[i_ner].split("-")[-1])
        #         ner_words = words[i_ner]
        #         for i in range(i_ner+1,end_ner+1):
        #             ner_words += words[i]
        #         ner_words += "-" + nertags[i_ner].split("-")[-1]
        #         ner_dict.append(ner_words)
        #         i_ner = end_ner+1
        #     else:
        #         i_ner += 1
        #
        # # 输出查询的年份
        # if "nt" in postags:
        #     search_year = words[postags.index("nt")]
        #     self.answer_edit.append("查询年份为：" + search_year)
        #
        # # 输出查询的学校,地区
        # # 先查看命名实体内
        # search_school = ""
        # search_district = ""
        # if len(ner_dict) != 0:
        #     for item in ner_dict:
        #         if item.find("Ni") != -1:
        #             search_school = item.split("-")[0]
        #         if item.find("Ns") != -1:
        #             search_district = item.split("-")[0]
        # # 再查看命名缩写
        # if search_school == "" and "j" in postags:
        #     search_school = words[postags.index("j")]
        #     print(search_school)
        # if search_district == "" and "ns" in postags:
        #     search_district = words[postags.index("ns")]
        # self.answer_edit.append("查询学校为：" + search_school)
        # self.answer_edit.append("查询地区为：" + search_district)
        # self.answer_edit.append(self.question_edit.text())

        # hanlp方法
        result = hanlp_nlp_segmentor(sentence)
        search_year = ""
        search_school = ""
        search_major = ""
        search_district = ""
        for item in result:
            # 词及其词性
            word = item.split("/")[0]
            nature = item.split("/")[-1]
            # 时间词（2015年、14年）
            if nature == "t":
                search_year = word
            # 识别词为nschool
            elif nature == "nschool":
                search_school = word
            # 识别词为nmajor
            elif nature == "nmajor":
                search_major = word
            # 识别词为地名
            elif nature == "ns":
                search_district = word
        # print(search_year+"--"+search_school+"--"+search_district+"--"+search_major)
        self.answer_edit.append("问句分析结果为：" + str(result))
        self.answer_edit.append("直接信息如下：")
        # self.answer_edit.append("查询类型为（mysql表（招生计划、录取分数）、图数据库）：")
        self.answer_edit.append("查询年份为：" + search_year)
        self.answer_edit.append("查询高校为：" + search_school)
        self.answer_edit.append("查询专业为：" + search_major)
        self.answer_edit.append("查询地区为：" + search_district)
        # self.answer_edit.append("查询结果为：")

        # 规范查询关键词
        # 年份（2017年、17年）
        # 去除"年"字
        if search_year.find("年") != -1:
            search_year = search_year.replace("年", "")

        # 高校（全称与简称）
        c9 = ["北京大学", "北京大学医学部", "清华大学", "复旦大学", "上海交通大学", "浙江大学",
              "南京大学", "中国科学技术大学", "哈尔滨工业大学", "西安交通大学"]
        c9_j = ["北大", "北大医学部", "清华", "复旦", "上交", "浙大",
                "南大", "中科大", "哈工大", "西交大"]
        if search_school in c9_j:
            search_school = c9[c9_j.index(search_school)]

        # 地区
        if search_district.find("省") != -1:
            search_district = search_district.replace("省", "")

        self.answer_edit.append("信息规范后如下：")
        # self.answer_edit.append("查询类型为（mysql表（招生计划、录取分数）、图数据库）：")
        self.answer_edit.append("查询年份为：" + search_year)
        self.answer_edit.append("查询高校为：" + search_school)
        self.answer_edit.append("查询专业为：" + search_major)
        self.answer_edit.append("查询地区为：" + search_district)

        # 构造SQL查询语句
        # 2017年哈工大软件工程在河南省招多少人？
        # SQL语句缺省查询
        # 只有年份,统计各学校的招生情况（文科、理科）
        if search_year != "" and search_school == "" and search_major == "" and search_district == "":
            # 查询学校该年招生总人数
            sql_string = "SELECT school,COUNT(*) FROM admission_plan WHERE year = '" + search_year \
                         + "' GROUP BY school;"
            myresult = self.mysql_query_sentence(sql_string)
            if len(myresult) == 0:
                self.answer_edit.append("查询结果为空！")
            else:
                for item in myresult:
                    self.answer_edit.append(str(item[0]) + search_year + "年" + "招生计划为" + str(item[1]) + "人")
                    # 查询该年该校招生的类别情况
                    sub_sql_string = "SELECT classy,COUNT(*) FROM admission_plan WHERE year = '" + search_year \
                                     + "' and school = '" + str(item[0]) + "' GROUP BY classy;"
                    print(sub_sql_string)
                    sub_myresult = self.mysql_query_sentence(sub_sql_string)
                    if len(sub_myresult) == 0:
                        self.answer_edit.append("招生类别查询结果为空！")
                    else:
                        for item in sub_myresult:
                            self.answer_edit.append("其中" + str(item[0]) + str(item[1]) + "人")
        # 只有学校，统计该学校的招生情况（文科理科）
        elif search_year == "" and search_school != "" and search_major == "" and search_district == "":
            # 查询学校各年招生总人数
            sql_string = "SELECT year,COUNT(*) FROM admission_plan WHERE school = '" + search_school \
                         + "' GROUP BY year;"
            myresult = self.mysql_query_sentence(sql_string)
            if len(myresult) == 0:
                self.answer_edit.append("查询结果为空！")
            else:
                for item in myresult:
                    self.answer_edit.append(search_school + str(item[0]) + "年" + "招生计划为" + str(item[1]) + "人")
                    # 查询该年该校招生的类别情况
                    sub_sql_string = "SELECT classy,COUNT(*) FROM admission_plan WHERE year = '" + str(item[0]) \
                                     + "' and school = '" + search_school + "' GROUP BY classy;"
                    # print(sub_sql_string)
                    sub_myresult = self.mysql_query_sentence(sub_sql_string)
                    if len(sub_myresult) == 0:
                        self.answer_edit.append("招生类别查询结果为空！")
                    else:
                        for item in sub_myresult:
                            self.answer_edit.append("其中" + str(item[0]) + "招生" + str(item[1]) + "人")
        # 只有专业，统计每年招生人数
        elif search_year == "" and search_school == "" and search_major != "" and search_district == "":
            # 查询该专业各校各年招生总人数
            sql_string = "SELECT year,COUNT(*) FROM admission_plan WHERE major = '" + search_major \
                         + "' GROUP BY year;"
            # print(sql_string)
            myresult = self.mysql_query_sentence(sql_string)
            if len(myresult) == 0:
                self.answer_edit.append("查询结果为空！")
            else:
                for item in myresult:
                    self.answer_edit.append(search_major + str(item[0]) + "招生" + str(item[1]) + "人")
                    sub_sql_string = "SELECT school,COUNT(*) FROM admission_plan WHERE major = '" + search_major \
                                     + "'and year = '" + str(item[0]) + "' GROUP BY school;"
                    sub_myresult = self.mysql_query_sentence(sub_sql_string)
                    if len(sub_myresult) == 0:
                        self.answer_edit.append("学校具体招生人数查询结果为空！")
                    else:
                        for item in sub_myresult:
                            self.answer_edit.append("其中" + str(item[0]) + "招生" + str(item[1]) + "人")
        # 只有地区，统计每年招生人数
        elif search_year == "" and search_school == "" and search_major == "" and search_district != "":
            # 查询该地区各年招生总人数
            sql_string = "SELECT year,COUNT(*) FROM admission_plan WHERE district = '" + search_district \
                         + "' GROUP BY year;"
            myresult = self.mysql_query_sentence(sql_string)
            if len(myresult) == 0:
                self.answer_edit.append("查询结果为空！")
            else:
                for item in myresult:
                    self.answer_edit.append(
                        "C9高校在" + search_district + str(item[0]) + "年" + "招生计划为" + str(item[1]) + "人")
                    # 查询该年某校招生的类别情况
                    sub_sql_string = "SELECT school,COUNT(*) FROM admission_plan WHERE district = '" \
                                     + search_district + "'and year = '" + str(item[0]) + "' GROUP BY school;"
                    # print(sub_sql_string)
                    sub_myresult = self.mysql_query_sentence(sub_sql_string)
                    if len(sub_myresult) == 0:
                        self.answer_edit.append("学校具体招生人数查询结果为空！")
                    else:
                        for item in sub_myresult:
                            self.answer_edit.append("其中" + str(item[0]) + "招生" + str(item[1]) + "人")
        # 只有年份和学校
        elif search_year != "" and search_school != "" and search_major == "" and search_district == "":
            # 查询学校该年招生总人数
            sql_string = "SELECT COUNT(*) FROM admission_plan WHERE year = '" + search_year \
                         + "' and school = '" + search_school + "' GROUP BY school;"
            myresult = self.mysql_query_sentence(sql_string)
            if len(myresult) == 0:
                self.answer_edit.append("查询结果为空！")
            else:
                self.answer_edit.append(search_school + search_year + "年" + "招生计划为" + str(myresult[0][0]) + "人")
                sub_sql_string = "SELECT classy,COUNT(*) FROM admission_plan WHERE year = '" + search_year \
                                 + "' and school = '" + search_school + "' GROUP BY classy;"
                print(sub_sql_string)
                sub_myresult = self.mysql_query_sentence(sub_sql_string)
                if len(sub_myresult) == 0:
                    self.answer_edit.append("学校具体招生人数查询结果为空！")
                else:
                    for item in sub_myresult:
                        self.answer_edit.append("其中" + str(item[0]) + str(item[1]) + "人")
        # 只有年份和专业
        elif search_year != "" and search_school == "" and search_major != "" and search_district == "":
            # 查询各学校该年该专业招生人数
            sql_string = "SELECT school,COUNT(*) FROM admission_plan WHERE year = '" + search_year \
                         + "' and major = '" + search_major + "' GROUP BY school;"
            myresult = self.mysql_query_sentence(sql_string)
            if len(myresult) == 0:
                self.answer_edit.append("查询结果为空！")
            else:
                for item in myresult:
                    self.answer_edit.append(
                        str(item[0]) + search_year + "年" + search_major + "招生计划为" + str(item[1]) + "人")
        # 只有年份和地区
        elif search_year != "" and search_school == "" and search_major == "" and search_district != "":
            # 查询各学校该年该地区招生人数
            sql_string = "SELECT school,COUNT(*) FROM admission_plan WHERE year = '" + search_year \
                         + "' and district = '" + search_district + "' GROUP BY school;"
            myresult = self.mysql_query_sentence(sql_string)
            if len(myresult) == 0:
                self.answer_edit.append("查询结果为空！")
            else:
                for item in myresult:
                    self.answer_edit.append(
                        str(item[0]) + search_year + "年" + "在" + search_district + "招生计划为" + str(item[1]) + "人")
        # 只有学校和专业
        elif search_year == "" and search_school != "" and search_major != "" and search_district == "":
            # 查询该学校各年该专业招生人数
            sql_string = "SELECT year,COUNT(*) FROM admission_plan WHERE school = '" + search_school \
                         + "' and major = '" + search_major + "' GROUP BY year;"
            myresult = self.mysql_query_sentence(sql_string)
            if len(myresult) == 0:
                self.answer_edit.append("查询结果为空！")
            else:
                for item in myresult:
                    self.answer_edit.append(
                        search_school + str(item[0]) + "年" + search_major + "招生计划为" + str(item[1]) + "人")
        # 只有学校和地区
        elif search_year == "" and search_school != "" and search_major == "" and search_district != "":
            # 查询该学校各年该地区招生人数
            sql_string = "SELECT year,COUNT(*) FROM admission_plan WHERE school = '" + search_school \
                         + "' and district = '" + search_district + "' GROUP BY year;"
            myresult = self.mysql_query_sentence(sql_string)
            if len(myresult) == 0:
                self.answer_edit.append("查询结果为空！")
            else:
                for item in myresult:
                    self.answer_edit.append(search_school + str(item[0]) + "年" + "在" + search_district
                                            + "招生计划为" + str(item[1]) + "人")
        # 只有专业和地区
        elif search_year == "" and search_school == "" and search_major != "" and search_district != "":
            # 查询各年该地区该专业招生人数
            sql_string = "SELECT year,COUNT(*) FROM admission_plan WHERE major = '" + search_major \
                         + "' and district = '" + search_district + "' GROUP BY year;"
            myresult = self.mysql_query_sentence(sql_string)
            if len(myresult) == 0:
                self.answer_edit.append("查询结果为空！")
            else:
                for item in myresult:
                    self.answer_edit.append(
                        str(item[0]) + "年" + search_major + "在" + search_district + "招生计划为" + str(item[1]) + "人")
                    # 查询该年各校的招生情况
                    sub_sql_string = "SELECT school,COUNT(*) FROM admission_plan WHERE major = '" + search_major \
                                     + "' and district = '" + search_district + "'and year = '" + str(item[0]) \
                                     + "' GROUP BY school;"
                    # print(sub_sql_string)
                    sub_myresult = self.mysql_query_sentence(sub_sql_string)
                    if len(sub_myresult) == 0:
                        self.answer_edit.append("学校具体招生人数查询结果为空！")
                    else:
                        for item in sub_myresult:
                            self.answer_edit.append("其中" + str(item[0]) + "招生" + str(item[1]) + "人")
        # 只有学校、专业、地区
        elif search_year == "" and search_school != "" and search_major != "" and search_district != "":
            # 查询该学校各年该专业该地区招生人数
            sql_string = "SELECT year,COUNT(*) FROM admission_plan WHERE school = '" + search_school \
                         + "' and major = '" + search_major + "' and district = '" + search_district \
                         + "' GROUP BY year;"
            myresult = self.mysql_query_sentence(sql_string)
            if len(myresult) == 0:
                self.answer_edit.append("查询结果为空！")
            else:
                for item in myresult:
                    self.answer_edit.append(search_school + str(item[0]) + "年" + "在" + search_district
                                            + search_major + "招生计划为" + str(item[1]) + "人")
        # 只有年份、专业、地区
        elif search_year != "" and search_school == "" and search_major != "" and search_district != "":
            # 查询各学校该年该专业该地区招生人数
            sql_string = "SELECT school,COUNT(*) FROM admission_plan WHERE year = '" + search_year \
                         + "' and major = '" + search_major + "' and district = '" + search_district \
                         + "' GROUP BY school;"
            myresult = self.mysql_query_sentence(sql_string)
            if len(myresult) == 0:
                self.answer_edit.append("查询结果为空！")
            else:
                for item in myresult:
                    self.answer_edit.append(str(item[0]) + search_year + "年" + "在" + search_district
                                            + search_major + "招生计划为" + str(item[1]) + "人")
        # 只有年份、学校、地区
        elif search_year != "" and search_school != "" and search_major == "" and search_district != "":
            # 查询该学校该年该地区招生人数
            sql_string = "SELECT classy,COUNT(*) FROM admission_plan WHERE year = '" + search_year \
                         + "' and school = '" + search_school + "' and district = '" + search_district \
                         + "' GROUP BY classy;"
            myresult = self.mysql_query_sentence(sql_string)
            if len(myresult) == 0:
                self.answer_edit.append("查询结果为空！")
            else:
                for item in myresult:
                    self.answer_edit.append(search_school + search_year + "年" + "在" + search_district
                                            + "招生" + str(item[0]) + "类" + str(item[1]) + "人")
        # 只有年份、学校、专业
        elif search_year != "" and search_school != "" and search_major != "" and search_district == "":
            # 查询该学校该年该专业招生人数
            sql_string = "SELECT district,COUNT(*) FROM admission_plan WHERE year = '" + search_year \
                         + "' and school = '" + search_school + "' and major = '" + search_major \
                         + "' GROUP BY district;"
            myresult = self.mysql_query_sentence(sql_string)
            if len(myresult) == 0:
                self.answer_edit.append("查询结果为空！")
            else:
                for item in myresult:
                    self.answer_edit.append(search_school + search_year + "年" + search_major
                                            + "在" + str(item[0]) + "招生" + str(item[1]) + "人")
        # 只有年份、学校、专业、地区
        elif search_year != "" and search_school != "" and search_major != "" and search_district != "":
            # 查询该学校该年该专业该地区招生情况
            sql_string = "SELECT classy,COUNT(*) FROM admission_plan WHERE school = '" + search_school \
                         + "' and year = '" + search_year + "' and major = '" + search_major \
                         + "' and district = '" + search_district + "' GROUP BY classy;"
            myresult = self.mysql_query_sentence(sql_string)
            if len(myresult) == 0:
                self.answer_edit.append("查询结果为空！")
            else:
                for item in myresult:
                    self.answer_edit.append(search_school + search_year + "年" + search_major + "在" + search_district
                                            + "招生" + str(item[0]) + "类" + str(item[1]) + "人")

    # 清空按钮状态
    def clear_button(self):
        self.ltp_result_dict.clear()
        if self.seg_btn.isChecked():
            self.seg_btn.click()
        if self.pos_btn.isChecked():
            self.pos_btn.click()
        if self.ner_btn.isChecked():
            self.ner_btn.click()
        self.question_edit.clear()
        self.answer_edit.clear()

    # mysql 查询语句,返回查询结果
    def mysql_query_sentence(self, mysql_string):
        dbname = "university_admission"
        mydb = connect_mysql_with_db(dbname)
        mycursor = mydb.cursor()
        mycursor.execute(mysql_string)
        myresult = mycursor.fetchall()
        return myresult


# MySQL表查看类
class MySQL_widgets(QWidget):
    # 构造方法
    def __init__(self):
        super().__init__()
        self.initUI()

    # GUI创建
    def initUI(self):
        self.create_MySQL_widgets()
        # 窗口信息设置
        self.setGeometry(200, 200, 500, 800)
        self.setWindowTitle("MySQL数据表查询")
        self.setWindowIcon(QIcon("images/cat.jpg"))
        self.show()

    # 创建MySQL查询控件
    def create_MySQL_widgets(self):
        table = QLabel("表类型")
        school = QLabel("学校")
        province = QLabel("地区")
        year = QLabel("年份")
        major = QLabel("专业")
        batch = QLabel("批次")
        classy = QLabel("科别")

        self.table_combo = QComboBox()
        table_names = ["计划招生", "专业分数", "地区分数"]
        self.table_combo.addItems(table_names)
        self.table_combo.activated[str].connect(self.table_combo_activated)

        self.school_combo = QComboBox()
        self.school_names = ["北京大学", "北京大学医学部", "清华大学", "复旦大学", "上海交通大学", "浙江大学",
                             "南京大学", "中国科学技术大学", "哈尔滨工业大学", "西安交通大学"]
        self.school_combo.addItems(self.school_names)
        self.school_combo.activated[str].connect(self.school_combo_activated)

        self.district_combo = QComboBox()
        self.district_names = ["北京", "天津"]
        self.district_combo.addItems(self.district_names)
        self.district_combo.activated[str].connect(self.district_combo_activated)

        self.year_combo = QComboBox()
        self.year_names = ["2018", "2017"]
        self.year_combo.addItems(self.year_names)
        self.year_combo.activated[str].connect(self.year_combo_activated)

        self.major_combo = QComboBox()
        self.major_names = ["计算机", "航天"]
        self.major_combo.addItems(self.major_names)

        self.batch_combo = QComboBox()
        self.batch_names = ["一批", "国家专项"]
        self.batch_combo.addItems(self.batch_names)

        self.classy_combo = QComboBox()
        self.classy_names = ["文史", "理工"]
        self.classy_combo.addItems(self.classy_names)

        select_hbox = QHBoxLayout()
        select_hbox.addWidget(table)
        select_hbox.addWidget(self.table_combo)
        select_hbox.addWidget(school)
        select_hbox.addWidget(self.school_combo)
        select_hbox.addWidget(province)
        select_hbox.addWidget(self.district_combo)
        select_hbox.addWidget(year)
        select_hbox.addWidget(self.year_combo)
        select_hbox.addWidget(major)
        select_hbox.addWidget(self.major_combo)
        select_hbox.addWidget(batch)
        select_hbox.addWidget(self.batch_combo)
        select_hbox.addWidget(classy)
        select_hbox.addWidget(self.classy_combo)

        SQL = QLabel("SQL语句")
        self.SQL_edit = QLineEdit()
        SQL_hbox = QHBoxLayout()
        SQL_hbox.addWidget(SQL)
        SQL_hbox.addWidget(self.SQL_edit)

        result = QLabel("查询结果")
        self.result_edit = QTextEdit()
        result_hbox = QHBoxLayout()
        result_hbox.addWidget(result)
        result_hbox.addWidget(self.result_edit)

        self.query_btn = QPushButton("查询")

        btn_hbox = QHBoxLayout()
        btn_hbox.addWidget(self.query_btn)
        self.query_btn.clicked.connect(self.mysql_query)

        main_vbox = QVBoxLayout()
        main_vbox.addLayout(select_hbox)
        main_vbox.addLayout(SQL_hbox)
        main_vbox.addLayout(result_hbox)
        main_vbox.addLayout(btn_hbox)
        self.setLayout(main_vbox)

    # mysql 查询语句,返回查询结果
    def mysql_query_sentence(self, mysql_string):
        dbname = "university_admission"
        mydb = connect_mysql_with_db(dbname)
        mycursor = mydb.cursor()
        mycursor.execute(mysql_string)
        myresult = mycursor.fetchall()
        return myresult

    # mysql查询
    def mysql_query(self):
        mysql_string = self.SQL_edit.text()
        if mysql_string != "":
            pass
        else:
            mysql_string = self.build_mysql_string()
            self.SQL_edit.setText(mysql_string)
        myresult = self.mysql_query_sentence(mysql_string)
        if len(myresult) == 0:
            self.result_edit.setText("查询结果为空！")
            return
        self.result_edit.clear()
        for item in myresult:
            self.result_edit.append(str(item))
        return myresult

    # 构造SQL语句
    def build_mysql_string(self):
        mysql_string = "select * from " + self.query_table_name + " where school='" + self.query_school_name \
                       + "' and district='" + self.query_district_name + "' and year='" + self.query_year_name \
                       + "';"
        return mysql_string

    # table_combo发生改变
    def table_combo_activated(self, text):
        table_names = ["计划招生", "专业分数", "地区分数"]
        mysql_table_name = ["admission_plan", "admission_score_major", "admission_score_pro"]
        self.query_table_name = mysql_table_name[table_names.index(text)]
        # 查询当前选择下（表名）学校数据项
        mysql_string = "select school from " + self.query_table_name + " group by school;"
        myresult = self.mysql_query_sentence(mysql_string)
        temp = []
        for item in myresult:
            temp.append(item[0])
        self.school_names = temp
        # 重新设置school_combo
        self.school_combo.clear()
        self.school_names = sorted(self.school_names, key=lambda x: lazy_pinyin(x.lower())[0][0])
        self.school_combo.addItems(self.school_names)

    # school_combo发生改变
    def school_combo_activated(self, text):
        self.query_school_name = text
        # 查询当前选择下（表名、学校）地区数据项
        mysql_string = "select district from " + self.query_table_name + " where school='" + self.query_school_name \
                       + "' group by district;"
        myresult = self.mysql_query_sentence(mysql_string)
        temp = []
        for item in myresult:
            temp.append(item[0])
        self.district_names = temp
        # 重新设置major_combo
        self.district_combo.clear()
        self.district_names = sorted(self.district_names, key=lambda x: lazy_pinyin(x.lower())[0][0])
        self.district_combo.addItems(self.district_names)

    # district_combo发生改变
    def district_combo_activated(self, text):
        self.query_district_name = text
        # 查询当前选择下（表名、学校、地区）年份数据项
        mysql_string = "select year from " + self.query_table_name + " where school='" + self.query_school_name \
                       + "' and district='" + self.query_district_name + "' group by year;"
        myresult = self.mysql_query_sentence(mysql_string)
        temp = []
        for item in myresult:
            temp.append(str(item[0]))
        self.year_names = temp
        # 重新设置year_combo
        self.year_combo.clear()
        self.year_names.sort()
        self.year_combo.addItems(self.year_names)

    # year_combo发生改变
    def year_combo_activated(self, text):
        self.query_year_name = text

        # 查询并设置major专业
        if self.query_table_name == "admission_score_pro":
            self.major_combo.clear()
            self.major_combo.addItem("无此项数据")
        else:
            mysql_string = "select major from " + self.query_table_name + " where school='" + self.query_school_name \
                           + "' and district='" + self.query_district_name + "' and year='" + self.query_year_name \
                           + "' group by major;"
            myresult = self.mysql_query_sentence(mysql_string)
            temp = []
            for item in myresult:
                temp.append(item[0])
            self.major_names = temp
            # 重新设置major_combo
            self.major_combo.clear()
            self.major_names = sorted(self.major_names, key=lambda x: lazy_pinyin(x.lower())[0][0])
            self.major_combo.addItems(self.major_names)

        # 查询并设置batch批次
        if self.query_table_name == "admission_score_pro":
            mysql_string = "select batch from " + self.query_table_name + " where school='" + self.query_school_name \
                           + "' and district='" + self.query_district_name + "' and year='" + self.query_year_name \
                           + "' group by batch;"
            myresult = self.mysql_query_sentence(mysql_string)
            temp = []
            for item in myresult:
                temp.append(item[0])
            self.batch_names = temp
            # 重新设置classy_combo
            self.batch_combo.clear()
            self.batch_names = sorted(self.batch_names, key=lambda x: lazy_pinyin(x.lower())[0][0])
            self.batch_combo.addItems(self.batch_names)
        else:
            self.batch_combo.clear()
            self.batch_combo.addItem("无此项数据")

        # 查询并设置classy科别
        mysql_string = "select classy from " + self.query_table_name + " where school='" + self.query_school_name \
                       + "' and district='" + self.query_district_name + "' and year='" + self.query_year_name \
                       + "' group by classy;"
        myresult = self.mysql_query_sentence(mysql_string)
        temp = []
        for item in myresult:
            temp.append(item[0])
        self.classy_names = temp
        # 重新设置classy_combo
        self.classy_combo.clear()
        self.classy_names = sorted(self.classy_names, key=lambda x: lazy_pinyin(x.lower())[0][0])
        self.classy_combo.addItems(self.classy_names)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    QAPage = QASystemMainWindow()
    sys.exit(app.exec_())
