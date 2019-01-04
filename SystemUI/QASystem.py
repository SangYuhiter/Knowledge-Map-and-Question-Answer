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
        self.setGeometry(300, 300, 500, 300)
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
        self.seg_btn = QPushButton('分词')
        self.seg_btn.setCheckable(True)
        self.seg_btn.clicked[bool].connect(self.ltp_op)
        self.pos_btn = QPushButton('词性标注')
        self.pos_btn.setCheckable(True)
        self.pos_btn.clicked[bool].connect(self.ltp_op)
        self.ner_btn = QPushButton('命名实体识别')
        self.ner_btn.setCheckable(True)
        self.ner_btn.clicked[bool].connect(self.ltp_op)

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

        vbox = QVBoxLayout()
        vbox.addStretch(1)
        vbox.addLayout(question_hbox)
        vbox.addStretch(1)
        vbox.addLayout(answer_hbox)
        vbox.addStretch(1)
        vbox.addLayout(button_box)
        vbox.addStretch(1)

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


# MySQL表查看
class MySQL_widgets(QWidget):
    # 构造方法
    def __init__(self):
        super().__init__()
        self.initUI()

    # GUI创建
    def initUI(self):
        self.create_MySQL_widgets()
        # 窗口信息设置
        self.setGeometry(300, 300, 500, 300)
        self.setWindowTitle("MySQL数据表查询")
        self.setWindowIcon(QIcon("images/cat.jpg"))
        self.show()

    # 创建MySQL查询控件
    def create_MySQL_widgets(self):
        table = QLabel("表类型")
        school = QLabel("学校")
        major = QLabel("专业")
        year = QLabel("年份")
        province = QLabel("地区")

        table_combo = QComboBox()
        table_names = ["计划招生", "专业分数", "地区分数"]
        table_combo.addItems(table_names)

        school_combo = QComboBox()
        school_names = ["北京大学", "清华大学", "复旦大学", "上海交通大学", "浙江大学",
                        "南京大学", "中国科学技术大学", "哈尔滨工业大学", "西安交通大学"]
        school_combo.addItems(school_names)

        major_combo = QComboBox()
        major_names = ["计算机", "航天"]
        major_combo.addItems(major_names)

        year_combo = QComboBox()
        year_names = ["2018", "2017"]
        year_combo.addItems(year_names)

        province_combo = QComboBox()
        province_names = ["北京", "天津"]
        province_combo.addItems(province_names)

        select_hbox = QHBoxLayout()
        select_hbox.addWidget(table)
        select_hbox.addWidget(table_combo)
        select_hbox.addWidget(school)
        select_hbox.addWidget(school_combo)
        select_hbox.addWidget(major)
        select_hbox.addWidget(major_combo)
        select_hbox.addWidget(year)
        select_hbox.addWidget(year_combo)
        select_hbox.addWidget(province)
        select_hbox.addWidget(province_combo)

        SQL = QLabel("SQL语句")
        SQL_edit = QLineEdit()
        SQL_hbox = QHBoxLayout()
        SQL_hbox.addWidget(SQL)
        SQL_hbox.addWidget(SQL_edit)

        result = QLabel("查询结果")
        result_edit = QTextEdit()
        result_hbox = QHBoxLayout()
        result_hbox.addWidget(result)
        result_hbox.addWidget(result_edit)

        query_btn = QPushButton("查询")
        btn_hbox = QHBoxLayout()
        btn_hbox.addWidget(query_btn)


        main_vbox = QVBoxLayout()
        main_vbox.addLayout(select_hbox)
        main_vbox.addLayout(SQL_hbox)
        main_vbox.addLayout(result_hbox)
        main_vbox.addLayout(btn_hbox)
        self.setLayout(main_vbox)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    QAPage = QASystemMainWindow()
    sys.exit(app.exec_())
