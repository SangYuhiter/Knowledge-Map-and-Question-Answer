# -*- coding: utf-8 -*-
"""
@File  : QASystem.py
@Author: SangYu
@Date  : 2018/12/28 13:42
@Desc  : 问答系统界面
"""
import sys
from PyQt5.QtWidgets import (QMainWindow, QApplication, QAction, qApp,
                             QLabel, QLineEdit, QWidget, QTextEdit, QComboBox, QHBoxLayout, QVBoxLayout,
                             QMessageBox, QDesktopWidget, QPushButton, QSplashScreen)
from PyQt5.QtGui import QIcon, QPixmap, QFont
from PyQt5.QtCore import Qt
from InformationGet.MysqlOperation import mysql_query_sentence
from pypinyin import lazy_pinyin
from TemplateLoad.QuestionTemplate import load_template_by_file, build_template_by_infos
from FileRead.FileNameRead import read_all_file_list
from QuestionAnswer.TemplateAnswerQuestion import answer_question_by_template
import time
from QuestionAnalysis.QuestionTypePredict import QTPredictKeyword, QTPredictTemplate, QTPredictModel


# 主界面
# noinspection PyArgumentList,PyCallByClass
class QASystemMainWindow(QMainWindow):
    # 构造方法
    def __init__(self):
        super().__init__()
        self.main_wid = None
        self.mysql_wid = None
        self.template_wid = None
        self.question_type_predict_keyword = None
        self.question_type_predict_template = None
        self.question_type_predict_model = None
        self.init_ui()

    # GUI创建
    def init_ui(self):
        # 创建菜单栏
        self.create_menu()
        # 创建工具栏
        self.create_tool()
        # 创建状态栏
        self.statusBar()

        # 问答组件
        self.main_wid = QAWidgets()
        self.setCentralWidget(self.main_wid)

        # 窗口信息设置
        self.setGeometry(300, 300, 800, 800)
        self.center()
        self.setWindowTitle("自动问答系统")
        self.setWindowIcon(QIcon("images/cat.jpg"))

    # 窗口居中
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    # 创建菜单栏
    def create_menu(self):
        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu('File')
        exit_menu = menu_bar.addMenu('Exit')

        # 查看数据库表
        mysql_act = QAction(QIcon('images/mysql.png'), 'MySQL', self)
        mysql_act.setShortcut('Ctrl+M')
        mysql_act.setStatusTip('MySQL Database')
        mysql_act.triggered.connect(self.turn_page_mysql)

        # 模板的查看与创建
        template_act = QAction(QIcon('images/template.png'), 'Template', self)
        template_act.setShortcut('Ctrl+T')
        template_act.setStatusTip('Template check&create')
        template_act.triggered.connect(self.turn_page_template)

        # 退出程序
        exit_act = QAction(QIcon('images/quit.png'), 'Exit', self)
        exit_act.setShortcut('Ctrl+Q')
        exit_act.setStatusTip('Exit application')
        exit_act.triggered.connect(self.close)

        exit_menu.addAction(exit_act)
        file_menu.addAction(mysql_act)
        file_menu.addAction(template_act)

    # 创建工具栏
    def create_tool(self):
        exit_act = QAction(QIcon('images/quit.png'), 'Exit', self)
        exit_act.setShortcut('Ctrl+Q')
        exit_act.setStatusTip('Exit application')
        exit_act.triggered.connect(self.close)

        toolbar = self.addToolBar('Exit')
        toolbar.addAction(exit_act)

    def pre_load_data(self, sp):
        self.question_type_predict_keyword = QTPredictKeyword()
        self.question_type_predict_template = QTPredictTemplate()
        self.question_type_predict_model = QTPredictModel()
        # 加载数据
        self.question_type_predict_keyword.pre_load_keyword()
        sp.showMessage("加载关键词标签映射...20%", Qt.AlignCenter, Qt.black)
        qApp.processEvents()
        self.question_type_predict_template.pre_load_question_template()
        sp.showMessage("加载问题模板标签映射...40%", Qt.AlignCenter, Qt.black)
        qApp.processEvents()
        self.question_type_predict_model.pre_load_jieba()
        sp.showMessage("加载结巴字典树...50%", Qt.AlignCenter, Qt.black)
        qApp.processEvents()
        self.question_type_predict_model.pre_load_stop_words()
        sp.showMessage("加载停用词典...60%", Qt.AlignCenter, Qt.black)
        qApp.processEvents()
        self.question_type_predict_model.pre_load_label_name_map()
        sp.showMessage("加载标签名字映射...70%", Qt.AlignCenter, Qt.black)
        qApp.processEvents()
        self.question_type_predict_model.pre_load_fastText_model()
        sp.showMessage("加载分类模型...100%", Qt.AlignCenter, Qt.black)
        qApp.processEvents()

    # 跳转到数据库查询界面
    def turn_page_mysql(self):
        self.mysql_wid = MySQLWidgets()
        self.mysql_wid.show()

    # 跳转到模板查看界面
    def turn_page_template(self):
        self.template_wid = TemplateCheckWidgets()
        self.template_wid.show()

    # 关闭窗口事件
    def closeEvent(self, event):
        reply = QMessageBox.question(self, '消息',
                                     "关闭系统吗？", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()


# QA部分控件
# noinspection PyArgumentList,PyUnresolvedReferences
class QAWidgets(QWidget):
    # 构造方法
    def __init__(self):
        super().__init__()
        self.clear_btn = None
        self.qa_btn = None
        self.question_edit = None
        self.answer_edit = None
        self.init_ui()

    # GUI创建
    def init_ui(self):
        self.create_qa_widgets()

    # 创建问答控件
    def create_qa_widgets(self):
        question = QLabel('Question')
        answer = QLabel('Answer')

        # 按钮
        self.clear_btn = QPushButton('清空')
        self.clear_btn.clicked.connect(self.clear_button)
        self.qa_btn = QPushButton('回答提问')
        self.qa_btn.clicked.connect(self.question_answer)

        # 编辑文本框
        self.question_edit = QLineEdit(self)
        self.answer_edit = QTextEdit(self)
        self.question_edit.returnPressed.connect(self.question_answer)

        # 布局方式
        question_hbox = QHBoxLayout()
        question_hbox.addWidget(question)
        question_hbox.addWidget(self.question_edit)

        answer_hbox = QHBoxLayout()
        answer_hbox.addWidget(answer)
        answer_hbox.addWidget(self.answer_edit)

        button_box = QHBoxLayout()
        button_box.addStretch(1)
        button_box.addWidget(self.clear_btn)
        button_box.addWidget(self.qa_btn)

        vbox = QVBoxLayout()
        vbox.addLayout(question_hbox)
        vbox.addLayout(answer_hbox)
        vbox.addLayout(button_box)

        self.setLayout(vbox)

    # 回答提出的问题
    def question_answer(self):
        self.answer_edit.clear()
        sentence = self.question_edit.text()
        sentence_type = self.question_type_predict(sentence)
        if sentence_type not in question_can_answer:
            self.answer_edit.append("抱歉，当前系统无法回答关于%s的问题，尝试问问其它问题！" % sentence_type)
        else:
            # hanlp方法
            mid_result, result_edit = answer_question_by_template(sentence)
            self.answer_edit.append("问句类型：" + sentence_type)
            self.answer_edit.append("分词列表：" + str(mid_result["segment_list"]))
            self.answer_edit.append("问题抽象结果：" + str(mid_result["ab_question"]))
            self.answer_edit.append("关键词列表：" + str(mid_result["keyword"]))
            self.answer_edit.append("正则化处理：" + str(mid_result["keyword_normalize"]))
            self.answer_edit.append("匹配问句模板：" + str(mid_result["match_template_question"]))
            self.answer_edit.append("匹配答句模板：" + str(mid_result["match_template_answer"]))
            if "mysql_string" in mid_result:
                self.answer_edit.append("查询语句：" + str(mid_result["mysql_string"]))
            if "search_result" in mid_result:
                self.answer_edit.append("查询结果：" + str(mid_result["search_result"]))
            self.answer_edit.append("回答如下：")
            for item in result_edit:
                self.answer_edit.append(item)

    # 判断问题类型,优先级：关键词>模板>模型
    def question_type_predict(self, sentence):
        # 使用关键词判断
        sentence_type = QAPage.question_type_predict_keyword.question_predict_by_keyword(sentence)
        if sentence_type:
            return sentence_type
        else:
            # 使用模板判断
            sentence_type = QAPage.question_type_predict_template.question_predict_by_template(sentence)
            if sentence_type:
                return sentence_type
            else:
                # 使用模型判断
                sentence_type = QAPage.question_type_predict_model.question_predict_by_fastText(sentence)
                return sentence_type

    # 清空按钮状态
    def clear_button(self):
        self.question_edit.clear()
        self.answer_edit.clear()


# MySQL表查看类
# noinspection PyArgumentList,PyUnresolvedReferences
class MySQLWidgets(QWidget):
    # 构造方法
    def __init__(self):
        super().__init__()
        self.table_combo = None
        self.school_combo = None
        self.district_combo = None
        self.year_combo = None
        self.major_combo = None
        self.batch_combo = None
        self.classy_combo = None
        self.SQL_edit = None
        self.result_edit = None
        self.query_btn = None
        self.query_table_name = None
        self.query_school_name = None
        self.query_district_name = None
        self.query_year_name = None
        self.query_major_name = None
        self.query_classy_name = None
        self.init_ui()

    # GUI创建
    def init_ui(self):
        self.create_mysql_widgets()
        # 窗口信息设置
        self.setGeometry(200, 200, 500, 800)
        self.setWindowTitle("MySQL数据表查询")
        self.setWindowIcon(QIcon("images/cat.jpg"))
        self.show()

    # 创建MySQL查询控件
    def create_mysql_widgets(self):
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
        self.school_combo.activated[str].connect(self.school_combo_activated)

        self.district_combo = QComboBox()
        self.district_combo.activated[str].connect(self.district_combo_activated)

        self.year_combo = QComboBox()
        self.year_combo.activated[str].connect(self.year_combo_activated)
        self.major_combo = QComboBox()
        self.major_combo.activated[str].connect(self.major_combo_activated)
        self.batch_combo = QComboBox()
        self.classy_combo = QComboBox()
        self.classy_combo.activated[str].connect(self.classy_combo_activated)

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

        sql = QLabel("SQL语句")
        self.SQL_edit = QLineEdit()
        sql_hbox = QHBoxLayout()
        sql_hbox.addWidget(sql)
        sql_hbox.addWidget(self.SQL_edit)

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
        main_vbox.addLayout(sql_hbox)
        main_vbox.addLayout(result_hbox)
        main_vbox.addLayout(btn_hbox)
        self.setLayout(main_vbox)

    # 设置SQL语句编辑框内的SQL语句
    def set_SQLedit_content(self):
        self.SQL_edit.clear()
        mysql_string = "select * from "
        if self.query_table_name is not None:
            mysql_string += self.query_table_name
        if self.query_school_name is not None:
            mysql_string += " where school='" + self.query_school_name + "'"
        if self.query_district_name is not None:
            mysql_string += " and district ='" + self.query_district_name + "'"
        if self.query_year_name is not None:
            mysql_string += " and year='" + self.query_year_name + "'"
        if self.query_major_name is not None:
            mysql_string += " and major='" + self.query_major_name + "'"
        if self.query_classy_name is not None:
            mysql_string += " and classy='" + self.query_classy_name + "'"
        mysql_string += ";"
        self.SQL_edit.setText(mysql_string)

    # mysql查询
    def mysql_query(self):
        mysql_string = self.SQL_edit.text()
        if mysql_string != "":
            pass
        else:
            mysql_string = self.build_mysql_string()
            self.SQL_edit.setText(mysql_string)
        myresult = mysql_query_sentence(mysql_string)
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
        myresult = mysql_query_sentence(mysql_string)
        temp = []
        for item in myresult:
            temp.append(item["school"])
        school_names = temp
        # 重新设置school_combo
        self.school_combo.clear()
        school_names = sorted(school_names, key=lambda x: lazy_pinyin(x.lower())[0][0])
        self.school_combo.addItems(school_names)
        self.set_SQLedit_content()

    # school_combo发生改变
    def school_combo_activated(self, text):
        self.query_school_name = text
        # 查询当前选择下（表名、学校）地区数据项
        mysql_string = "select district from " + self.query_table_name + " where school='" + self.query_school_name \
                       + "' group by district;"
        myresult = mysql_query_sentence(mysql_string)
        temp = []
        for item in myresult:
            temp.append(item["district"])
        district_names = temp
        # 重新设置major_combo
        self.district_combo.clear()
        district_names = sorted(district_names, key=lambda x: lazy_pinyin(x.lower())[0][0])
        self.district_combo.addItems(district_names)
        self.set_SQLedit_content()

    # district_combo发生改变
    def district_combo_activated(self, text):
        self.query_district_name = text
        # 查询当前选择下（表名、学校、地区）年份数据项
        mysql_string = "select year from " + self.query_table_name + " where school='" + self.query_school_name \
                       + "' and district='" + self.query_district_name + "' group by year;"
        myresult = mysql_query_sentence(mysql_string)
        temp = []
        for item in myresult:
            temp.append(str(item["year"]))
        year_names = temp
        # 重新设置year_combo
        self.year_combo.clear()
        year_names.sort()
        self.year_combo.addItems(year_names)
        self.set_SQLedit_content()

    # year_combo发生改变
    def year_combo_activated(self, text):
        self.query_year_name = text
        self.set_SQLedit_content()

        # 查询并设置major专业
        if self.query_table_name == "admission_score_pro":
            self.major_combo.clear()
            self.major_combo.addItem("无此项数据")
        else:
            mysql_string = "select major from " + self.query_table_name + " where school='" + self.query_school_name \
                           + "' and district='" + self.query_district_name + "' and year='" + self.query_year_name \
                           + "' group by major;"
            myresult = mysql_query_sentence(mysql_string)
            temp = []
            for item in myresult:
                temp.append(item["major"])
            major_names = temp
            # 重新设置major_combo
            self.major_combo.clear()
            major_names = sorted(major_names, key=lambda x: lazy_pinyin(x.lower())[0][0])
            self.major_combo.addItems(major_names)

        # 查询并设置batch批次
        if self.query_table_name == "admission_score_pro":
            mysql_string = "select batch from " + self.query_table_name + " where school='" + self.query_school_name \
                           + "' and district='" + self.query_district_name + "' and year='" + self.query_year_name \
                           + "' group by batch;"
            myresult = mysql_query_sentence(mysql_string)
            temp = []
            for item in myresult:
                temp.append(item["batch"])
            batch_names = temp
            # 重新设置classy_combo
            self.batch_combo.clear()
            batch_names = sorted(batch_names, key=lambda x: lazy_pinyin(x.lower())[0][0])
            self.batch_combo.addItems(batch_names)
        else:
            self.batch_combo.clear()
            self.batch_combo.addItem("无此项数据")

        # 查询并设置classy科别
        mysql_string = "select classy from " + self.query_table_name + " where school='" + self.query_school_name \
                       + "' and district='" + self.query_district_name + "' and year='" + self.query_year_name \
                       + "' group by classy;"
        myresult = mysql_query_sentence(mysql_string)
        temp = []
        for item in myresult:
            temp.append(item["classy"])
        classy_names = temp
        # 重新设置classy_combo
        self.classy_combo.clear()
        classy_names = sorted(classy_names, key=lambda x: lazy_pinyin(x.lower())[0][0])
        self.classy_combo.addItems(classy_names)

    # major_combo发生改变
    def major_combo_activated(self, text):
        if text != "":
            self.query_major_name = text
            self.set_SQLedit_content()

    # classy_combo发生改变
    def classy_combo_activated(self, text):
        if text != "":
            self.query_classy_name = text
            self.set_SQLedit_content()


# Template查看与创建控件
# noinspection PyArgumentList,PyUnresolvedReferences
class TemplateCheckWidgets(QWidget):
    # 构造方法
    def __init__(self):
        super().__init__()
        self.query_current_template_btn = None
        self.template_combo = None
        self.template_fields_edit = None
        self.template_sentence_edit = None
        self.build_template_btn = None
        self.template_build_wid = None
        self.init_ui()

    # GUI创建
    def init_ui(self):
        self.create_template_check_widgets()
        # 窗口信息设置
        self.setGeometry(200, 200, 1000, 800)
        self.setWindowTitle("模板查看")
        self.setWindowIcon(QIcon("images/cat.jpg"))
        self.show()

    # 创建模板查看与创建控件
    def create_template_check_widgets(self):
        # 当前模板查看（查询按钮+模板显示下拉框、横向布局）
        self.query_current_template_btn = QPushButton("查看当前模板")
        self.query_current_template_btn.clicked.connect(self.template_query)

        current_template_text = QLabel("当前模板")
        self.template_combo = QComboBox()
        self.template_combo.activated[str].connect(self.template_combo_activated)

        select_hbox = QHBoxLayout()
        select_hbox.addWidget(self.query_current_template_btn)
        select_hbox.addWidget(current_template_text)
        select_hbox.addWidget(self.template_combo)

        # 模板字段部分
        template_fields_text = QLabel("模板字段")
        self.template_fields_edit = QTextEdit()

        template_fields_hbox = QHBoxLayout()
        template_fields_hbox.addWidget(template_fields_text)
        template_fields_hbox.addWidget(self.template_fields_edit)

        # 模板句式部分
        template_sentence_text = QLabel("模板句式")
        self.template_sentence_edit = QTextEdit()

        template_sentence_hbox = QHBoxLayout()
        template_sentence_hbox.addWidget(template_sentence_text)
        template_sentence_hbox.addWidget(self.template_sentence_edit)

        # 创建模板
        self.build_template_btn = QPushButton("创建模板")
        self.build_template_btn.clicked.connect(self.turn_page_template_build)
        template_build_hbox = QHBoxLayout()
        template_build_hbox.addWidget(self.build_template_btn)

        main_vbox = QVBoxLayout()
        main_vbox.addLayout(select_hbox)
        main_vbox.addLayout(template_fields_hbox)
        main_vbox.addLayout(template_sentence_hbox)
        main_vbox.addLayout(template_build_hbox)
        self.setLayout(main_vbox)

    # 查看当前模板
    def template_query(self):
        template_path = "../TemplateLoad/Template"
        file_list = read_all_file_list(template_path)
        template_file = [file.split("\\")[-1] for file in file_list]
        self.template_combo.clear()
        self.template_combo.addItems(template_file)

    # 当点击某个模板时
    def template_combo_activated(self, text):
        template_path = "../TemplateLoad/Template"
        fq_condition, fq_target, ts_answers, ts_questions = load_template_by_file(template_path + "/" + text)
        self.template_fields_edit.clear()
        self.template_fields_edit.append("问句条件词：")
        self.template_fields_edit.append(str(fq_condition))
        self.template_fields_edit.append("问句目标词：")
        for word in fq_target:
            self.template_fields_edit.append(word)

        self.template_sentence_edit.clear()
        self.template_sentence_edit.append("答句模板：")
        for sentence in ts_answers:
            self.template_sentence_edit.append(sentence)
        self.template_sentence_edit.append("问句模板：")
        for sentence in ts_questions:
            self.template_sentence_edit.append(sentence)

    # 跳转到模板创造页面
    def turn_page_template_build(self):
        self.template_build_wid = TemplateBuildWidgets()
        self.template_build_wid.show()


# Template创建控件
# noinspection PyArgumentList
class TemplateBuildWidgets(QWidget):
    # 构造方法
    def __init__(self):
        super().__init__()
        self.template_name_edit = None
        self.fq_condition_edit = None
        self.fq_target_edit = None
        self.template_sentence_edit = None
        self.input_btn = None
        self.analysis_result = None
        self.build_template_btn = None
        self.template_build_result_edit = None
        self.init_ui()

    # GUI创建
    def init_ui(self):
        self.create_template_build_widgets()
        # 窗口信息设置
        self.setGeometry(200, 200, 1000, 800)
        self.setWindowTitle("模板创建")
        self.setWindowIcon(QIcon("images/cat.jpg"))
        self.show()

    # 创建模板查看与创建控件
    def create_template_build_widgets(self):
        # 输入模板名
        tip_name_text = QLabel("请在以下文本框中输入模板名")
        tip_name_hbox = QHBoxLayout()
        tip_name_hbox.addWidget(tip_name_text)
        template_name_text = QLabel("模板名")
        self.template_name_edit = QLineEdit()
        template_name_hbox = QHBoxLayout()
        template_name_hbox.addWidget(template_name_text)
        template_name_hbox.addWidget(self.template_name_edit)

        # 输入问句条件词
        tip_fq_condition_text = QLabel("输入问句条件词（英文名称在前且唯一，后面可跟多个中文解释）如：\n"
                                       "school 学校 高校")
        tip_fq_condition_hbox = QHBoxLayout()
        tip_fq_condition_hbox.addWidget(tip_fq_condition_text)
        fq_condition_text = QLabel("问句条件词")
        self.fq_condition_edit = QTextEdit()
        fq_condition_hbox = QHBoxLayout()
        fq_condition_hbox.addWidget(fq_condition_text)
        fq_condition_hbox.addWidget(self.fq_condition_edit)

        # 输入问句目标词
        tip_fq_target_text = QLabel("输入问句目标词（英文名称在前且唯一，后面可跟多个中文解释）如：\n"
                                    "numbers 招生人数 招生计划 招多少人 招生计划是多少 招生人数是多少")
        tip_fq_target_hbox = QHBoxLayout()
        tip_fq_target_hbox.addWidget(tip_fq_target_text)
        fq_target_text = QLabel("问句目标词")
        self.fq_target_edit = QTextEdit()
        fq_target_hbox = QHBoxLayout()
        fq_target_hbox.addWidget(fq_target_text)
        fq_target_hbox.addWidget(self.fq_target_edit)

        # 输入问句模板及对应的答句模板
        tip_template_sentence_text = QLabel("每行输入完整的模板句示例及对应的答案句模板，如：\n"
                                            "(school)(year)(major)(district)(classy)(numbers)\n"
                                            "(school)(year)(major)(district)(classy)招收(numbers)人")
        tip_template_sentence_hbox = QHBoxLayout()
        tip_template_sentence_hbox.addWidget(tip_template_sentence_text)
        template_sentence_text = QLabel("模板字段")
        self.template_sentence_edit = QTextEdit()
        template_sentence_hbox = QHBoxLayout()
        template_sentence_hbox.addWidget(template_sentence_text)
        template_sentence_hbox.addWidget(self.template_sentence_edit)

        self.input_btn = QPushButton("输入以上信息")
        self.input_btn.clicked.connect(self.analysis_input)
        input_btn_hbox = QHBoxLayout()
        input_btn_hbox.addWidget(self.input_btn)

        # 分析字段并返回给用户
        analysis_result_text = QLabel("字段分析结果")
        self.analysis_result = QTextEdit()
        analysis_result_hbox = QHBoxLayout()
        analysis_result_hbox.addWidget(analysis_result_text)
        analysis_result_hbox.addWidget(self.analysis_result)

        # 字段确认，进入模板构造阶段
        self.build_template_btn = QPushButton("模板构造")
        self.build_template_btn.clicked.connect(self.build_template)
        build_template_btn_hbox = QHBoxLayout()
        build_template_btn_hbox.addWidget(self.build_template_btn)

        # 构造模板显示
        template_build_result_text = QLabel("构造模板")
        self.template_build_result_edit = QTextEdit()
        template_build_result_hbox = QHBoxLayout()
        template_build_result_hbox.addWidget(template_build_result_text)
        template_build_result_hbox.addWidget(self.template_build_result_edit)

        main_vbox = QVBoxLayout()
        main_vbox.addLayout(tip_name_hbox)
        main_vbox.addLayout(template_name_hbox)
        main_vbox.addLayout(tip_fq_condition_hbox)
        main_vbox.addLayout(fq_condition_hbox)
        main_vbox.addLayout(tip_fq_target_hbox)
        main_vbox.addLayout(fq_target_hbox)
        main_vbox.addLayout(tip_template_sentence_hbox)
        main_vbox.addLayout(template_sentence_hbox)
        main_vbox.addLayout(input_btn_hbox)
        main_vbox.addLayout(analysis_result_hbox)
        main_vbox.addLayout(build_template_btn_hbox)
        main_vbox.addLayout(template_build_result_hbox)
        self.setLayout(main_vbox)

    # 确认用户输入字段，返回分析结果
    def analysis_input(self):
        name = self.template_name_edit.text()
        fq_condition = self.fq_condition_edit.toPlainText().strip()
        fq_target = self.fq_target_edit.toPlainText().strip()
        template_sentence = self.template_sentence_edit.toPlainText().strip().replace("（", "(").replace("）", ")")
        self.analysis_result.clear()
        if name == "":
            self.analysis_result.append("模板名为空！")
        else:
            self.analysis_result.append("模板名:" + name)
        if fq_condition == "":
            self.analysis_result.append("问句条件词为空！")
        else:
            self.analysis_result.append("问句条件词：")
            fq_condition_list = fq_condition.split("\n")
            for fqc in fq_condition_list:
                self.analysis_result.append(fqc)
        if fq_target == "":
            self.analysis_result.append("问句目标词为空！")
        else:
            self.analysis_result.append("问句目标词：")
            fq_target_list = fq_target.split("\n")
            for fqt in fq_target_list:
                self.analysis_result.append(fqt)
        if template_sentence == "":
            self.analysis_result.append("答句模板为空！")
        else:
            self.analysis_result.append("答句模板：")
            template_sentence_list = template_sentence.split("\n")
            for sentence in template_sentence_list:
                self.analysis_result.append(sentence)
        self.analysis_result.append("请确认以上字段对应关系和模板句，确认无误后点击模板构造按钮")

    # 构造模板
    def build_template(self):
        name = self.template_name_edit.text()
        fq_condition = self.fq_condition_edit.toPlainText().strip()
        fq_target = self.fq_target_edit.toPlainText().strip()
        template_sentence = self.template_sentence_edit.toPlainText().strip().replace("（", "(").replace("）", ")")

        self.template_build_result_edit.clear()
        if name == "":
            self.template_build_result_edit.append("模板名为空！")
        elif fq_condition == "":
            self.template_build_result_edit.append("问句条件词为空！")
        elif fq_target == "":
            self.template_build_result_edit.append("问句目标词为空！")
        elif template_sentence == "":
            self.template_build_result_edit.append("答句模板为空！")
        if name == "" or fq_condition == "" or fq_target == "" or template_sentence == "":
            self.template_build_result_edit.append("请填充以上为空的模块后再构造模板！")

        if name != "" and fq_condition != "" and fq_target != "" and template_sentence != "":
            fq_condition_list = fq_condition.split("\n")
            fq_target_list = fq_target.split("\n")
            template_sentence_list = template_sentence.split("\n")
            ts_question = [template_sentence_list[i_question]
                           for i_question in range(0, len(template_sentence_list), 2)]
            ts_answer = [template_sentence_list[i_answer]
                         for i_answer in range(1, len(template_sentence_list), 2)]
            template_root_path = "../TemplateLoad/Template"
            build_template_by_infos(template_root_path + "/" + name, fq_condition_list, fq_target_list, ts_question,
                                    ts_answer)
            self.template_build_result_edit.clear()
            self.template_build_result_edit.append("构造的模板句式如下：")
            fq_condition, fq_target, ts_answers, ts_questions \
                = load_template_by_file(template_root_path + "/" + name)
            self.template_build_result_edit.append("模板答案句如下：")
            for i_answer in range(len(ts_answers)):
                self.template_build_result_edit.append(str(i_answer) + "--" + ts_answers[i_answer])
            self.template_build_result_edit.append("模板问题句如下：")
            for sentence in ts_questions:
                self.template_build_result_edit.append(sentence)


if __name__ == "__main__":
    # 当前能够回答的问题
    question_can_answer = ["录取分数", "招生计划"]

    app = QApplication(sys.argv)
    # 预加载数据界面
    splash = QSplashScreen(QPixmap("images/cat.jpg"))
    splash.show()  # 显示启动界面
    font = QFont()
    font.setPointSize(16)
    font.setBold(True)
    font.setWeight(75)
    splash.setFont(font)
    splash.showMessage("加载... 0%", Qt.AlignCenter, Qt.black)
    qApp.processEvents()  # 处理主进程事件
    # 界面开始执行
    QAPage = QASystemMainWindow()
    QAPage.pre_load_data(splash)
    QAPage.show()
    splash.finish(QAPage)
    sys.exit(app.exec_())
