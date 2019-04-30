# -*- coding: utf-8 -*-
"""
@File  : GetFrequentQuestion.py
@Author: SangYu
@Date  : 2019/3/15 13:54
@Desc  : 获取常见问题集
"""
from bs4 import BeautifulSoup
from InformationGet.InternetConnect import request_url, selenium_chrome
from Log.Logger import MyLog
import sys
import time
import csv
import pickle
from threading import Thread
import threading
from queue import Queue
import os
import random


# 从阳光高考网获取常见问题集
# noinspection PyProtectedMember,PyUnusedLocal
def get_question_yggk():
    function_logger = MyLog(logger=sys._getframe().f_code.co_name).getlog()
    # 院校咨询页url
    main_url = "https://gaokao.chsi.com.cn"
    file_path = "Information/大学/Test"
    allready_get = [
        ["北京大学", str(26232)], ["哈尔滨工业大学", str(26617)], ["北京大学医学部", str(6405529)],
        ["上海交通大学", str(6217)], ["上海交通大学医学院", str(61811)], ["清华大学", str(36710)],
        ["复旦大学", str(7243)], ["南京大学", str(4453)], ["浙江大学", str(43617)], ["中国科学技术大学", str(6280)],
        ["哈尔滨工业大学(威海)", str(62646117)], ["西安交通大学", str(53593)]
    ]
    university_formid = []
    with open("Information/大学/university_info", "rb")as p_file:
        university_infos = pickle.load(p_file)
    for info in university_infos:
        if "985" in info["院校特性"] or "211" in info["院校特性"]:
            if info["forum_id"] != "":
                university_formid.append([info["院校名称"], info["forum_id"]])
    function_logger.info("共有%d所985、211大学" % len(university_formid))
    for university in university_formid:
        begin = time.time()
        function_logger.info("开始抓取" + university[0] + "的招生问题数据...")
        main_page_url = "https://gaokao.chsi.com.cn/zxdy/forum--method-listDefault,year-2005,forumid-" + university[
            1] + ",start-0.dhtml"
        try:
            main_page_source = request_url(main_page_url)
            main_page_source.encoding = main_page_source.apparent_encoding
            main_page_soup = BeautifulSoup(main_page_source.content, "lxml")
            # 获取页面总数，页面栏含有省略号、不含省略号两种查找方式
            if main_page_soup.find("li", class_="lip dot"):
                page_count = main_page_soup.find("li", class_="lip dot").next_sibling.a.string
            else:
                page_count = main_page_soup.find("ul", class_="ch-page clearfix").find_all("li")[-2].a.string
            # 置顶问题个数
            top_question_count = len(main_page_soup.find("table", class_="ch-table zx-table")
                                     .find_all("span", class_="question_top_txt"))
            function_logger.debug("页面总数：%d 置顶问题个数：%d" % (int(page_count), int(top_question_count)))
        except Exception as e:
            # 招生咨询页面没有数据（三个大学）
            function_logger.error("%s咨询界面没有数据，页面链接为：%s" % (university[0], main_page_url))
            function_logger.error("错误信息：%s" % e)
            continue
        # 创建该学校的问题集收集表,并写好表头
        table_head = ["标题", "来源", "时间", "问题", "回答"]
        csvfile = open(file_path + "/" + university[0] + "常用问题集.csv", "w", newline="", encoding='utf-8')
        csvfile.truncate()
        writer = csv.writer(csvfile)
        writer.writerow(table_head)
        record_queue = Queue()
        # 每次开启10个线程,进行数据下载和存储
        start_index = 0
        end_index = 10
        while True:
            if start_index > int(page_count):
                break
            else:
                dThread = [DownloadPageInfo(university[1], page_id, int(page_count), top_question_count, record_queue)
                           for page_id in
                           range(start_index, end_index)]
                sThread = SavePageInfo(record_queue, writer)
                for d in dThread:
                    d.start()
                sThread.start()
                for d in dThread:
                    d.join()
                record_queue.put(-1)
                sThread.join()
                start_index += 10
                end_index += 10
                if end_index > int(page_count):
                    end_index = int(page_count)

        csvfile.close()
        function_logger.info("抓取%s的信息用时：%ds" % (university[0], time.time() - begin))


# 下载一页的信息
class DownloadPageInfo(Thread):
    def __init__(self, university_id, page_id, page_count, top_question_count, record_queue):
        Thread.__init__(self)
        self.university_id = university_id
        self.page_id = page_id
        self.page_count = page_count
        self.top_question_count = top_question_count
        self.record_queue = record_queue
        self.thread_logger = MyLog(logger="thread" + str(threading.current_thread().ident)).getlog()

    def get_page_info(self):
        main_url = "https://gaokao.chsi.com.cn"
        page_question_count = 15
        page_url = main_url + "/zxdy/forum--method-listDefault,year-2005,forumid-" + self.university_id + ",start-" + str(
            self.page_id * page_question_count) + ".dhtml"
        self.thread_logger.info("页面抓取进度(%d,%d)" % (self.page_id + 1, self.page_count))
        self.thread_logger.info("页面url %s" % page_url)
        try:
            page_source = request_url(page_url)
            page_source.encoding = page_source.apparent_encoding
            page_soup = BeautifulSoup(page_source.text, "lxml")
            # 获取咨询序列（所有的子节点）
            tr_list = page_soup.find("table", class_="ch-table zx-table").contents
            # 除去其中的空行
            for item in tr_list:
                if item == "\n":
                    tr_list.remove(item)
            # 置顶问答只记录一次
            if self.page_id == 0:
                start_index = 0
            else:
                start_index = self.top_question_count * 2
            page_infos = []
            for i_qa_pair in range(start_index, len(tr_list), 2):
                question_title = "q_title"
                question_from = ""
                question_time = ""
                question_text = "q_text"
                answer_text = "a_text"
                question_title = str(tr_list[i_qa_pair].find("a", class_="question_t_txt").string).strip().replace(",",
                                                                                                                   "，")
                # self.thread_logger.debug("标题:%s" % question_title)
                question_from = str(tr_list[i_qa_pair].find("i", title="提问人").next_sibling.string).strip().replace(",",
                                                                                                                   "，")
                # self.thread_logger.debug("来源:%s" % question_from)
                question_time = str(
                    tr_list[i_qa_pair].find("td", class_="question_t ch-table-center").text).strip().replace(",", "，")
                # self.thread_logger.debug("时间:%s" % question_time)
                # 问题与答案可能出现本页无法写下的情况，需要进行页面跳转获取信息
                question_text_class = tr_list[i_qa_pair + 1].find("div", class_="question")
                if question_text_class.find(text='[详细]') is None:
                    question_text = str(question_text_class.text).strip()
                else:
                    turn_page_url = main_url + question_text_class.find("a", text='[详细]')["href"]
                    question_text = self.get_question_text(turn_page_url)
                replace_str = ["回复", "\n", "\r", "\t", "\xa0", "\ue63c", "\ue5e5", "\u3000" "[", "]", " "]
                for r_str in replace_str:
                    question_text = question_text.replace(r_str, "")
                question_text.replace(",", "，")
                # self.thread_logger.debug("问题:%s" % question_text)
                answer_text_class = tr_list[i_qa_pair + 1].find("div", class_="question_a")
                if answer_text_class.find(text='[详细]') is None:
                    answer_text = str(answer_text_class.text).replace("[ 回复 ]", "").strip()
                else:
                    turn_page_url = main_url + answer_text_class.find("a", text='[详细]')["href"]
                    answer_text = self.get_answer_text(turn_page_url)
                replace_str = ["回复", "\n", "\r", "\t", "\xa0", "\ue63c", "\ue5e5", "\u3000" "[", "]", " "]
                for r_str in replace_str:
                    answer_text = answer_text.replace(r_str, "")
                answer_text.replace(",", "，")
                # self.thread_logger.debug("回答:%s" % answer_text)
                page_infos.append([question_title, question_from, question_time, question_text, answer_text])
            return page_infos

        except Exception as e:
            self.thread_logger.error("错误信息%s" % e)
            return []

    def get_question_text(self, turn_page_url):
        try:
            turn_page_source = request_url(turn_page_url)
            turn_page_source.encoding = turn_page_source.apparent_encoding
            turn_page_soup = BeautifulSoup(turn_page_source.text, "lxml")
            question_text = str(turn_page_soup.find("div", class_="question").text).strip()
            return question_text
        except Exception as e:
            self.thread_logger.error("问句%s抓取失败,失败原因%s" % (turn_page_url, e))
            return ""

    def get_answer_text(self, turn_page_url):
        try:
            turn_page_source = request_url(turn_page_url)
            turn_page_source.encoding = turn_page_source.apparent_encoding
            turn_page_soup = BeautifulSoup(turn_page_source.text, "lxml")
            answer_text = str(turn_page_soup.find("div", class_="question_a").text).strip()
            return answer_text
        except Exception as e:
            self.thread_logger.error("答句%s抓取失败,失败原因%s" % (turn_page_url, e))
            return ""

    def run(self):
        page_record = self.get_page_info()
        if page_record:
            self.record_queue.put(page_record)


# 保存页面信息的线程
class SavePageInfo(Thread):
    def __init__(self, record_queue, writer):
        Thread.__init__(self)
        self.record_queue = record_queue
        self.writer = writer
        self.flag = 1

    def save_page_info(self, page_record):
        self.flag = 0
        for record in page_record:
            self.writer.writerow(record)
        self.flag = 1

    def run(self):
        while True:
            page_record = self.record_queue.get()
            if page_record == -1:
                break
            if page_record and self.flag:
                self.save_page_info(page_record)


# 从阳光高考网上获取本科大学（能够筛选出985、211）的院校代码信息
def get_undergraduate_university_info():
    # 院校库主页
    function_logger = MyLog(logger=sys._getframe().f_code.co_name).getlog()
    main_url = "https://gaokao.chsi.com.cn/sch/search.do?searchType=1&xlcc=bk&start="
    main_page_source = request_url(main_url + "0")
    main_page_source.encoding = main_page_source.apparent_encoding
    main_page_soup = BeautifulSoup(main_page_source.text, "lxml")
    page_count = int(main_page_soup.find("li", class_="lip dot").next_sibling.text)
    page_university_count = 20
    university_infos = []
    for i_page in range(page_count):
        page_url = main_url + str(i_page * page_university_count)
        function_logger.info("页面抓取进度(%d,%d)" % (i_page + 1, int(page_count)))
        function_logger.info("页面url%s" % page_url)
        browser = selenium_chrome(page_url)
        page_souce = browser.find_element_by_class_name("ch-table").get_attribute("innerHTML")
        browser.quit()
        page_soup = BeautifulSoup(page_souce, "lxml")
        page_soup.prettify()
        head = [th.text for th in page_soup.find("tr").find_all("th")]
        print(head)
        for tr in page_soup.find_all("tr")[1:]:
            info = {}
            td_list = tr.find_all("td")
            info["url"] = "https://gaokao.chsi.com.cn" + td_list[0].find("a")["href"]
            for i in [0, 1, 2, 3, 4, 7]:
                info[head[i]] = td_list[i].text.strip()
            info[head[5]] = td_list[5].text.strip().replace("\n", "").replace(" ", "").replace("\u2002", " ")
            info[head[6]] = td_list[6].text.strip().replace("\ue664", "有") if td_list[6].text.strip() != "" else "无"
            university_infos.append(info)
    for info in university_infos:
        print(info)
    with open("Information/大学/university_info", "wb")as p_file:
        pickle.dump(university_infos, p_file)


# 从阳光高考网上获取学校咨询论坛的id
def get_consultation_forum_id():
    with open("Information/大学/university_info", "rb")as p_file:
        university_infos = pickle.load(p_file)
    for i_info in range(len(university_infos)):
        info = university_infos[i_info]
        # if "985" not in info["院校特性"] and "211" not in info["院校特性"]:
        #     continue
        print(info)
        try:
            page_source = request_url(info["url"])
            page_source.encoding = page_source.apparent_encoding
            forum_id = \
                BeautifulSoup(page_source.text, "lxml").find("a", class_="ch-btn zx-question")["href"].split("-")[-1][
                :-6]
            print(forum_id)
        except:
            forum_id = ""
        university_infos[i_info]["forum_id"] = forum_id
    with open("Information/大学/university_info", "wb")as p_file:
        pickle.dump(university_infos, p_file)
    for info in university_infos:
        if "985" in info["院校特性"] and "211" in info["院校特性"]:
            print(info)


# 对抓取的985，211常用问题集进行预处理,去除不满足条件的记录（不足五个字段）
def pretreat_crawl_questions():
    function_logger = MyLog(logger=sys._getframe().f_code.co_name).getlog()
    data_dir = "Information/大学/常问问题集/Data"
    pickle_dir = "Information/大学/常问问题集/Pickle"
    file_list = os.listdir(data_dir)
    function_logger.debug("大学数量：%d" % len(file_list))
    for file in file_list:
        university_name = file[:-9]
        function_logger.debug(university_name)
        function_logger.info("开始读取%s的常问问题集..." % university_name)
        with open(data_dir + "/" + file, "r", encoding="utf-8") as csvfile:
            csv_reader = csv.reader(csvfile)
            fqa_lines = []
            for row in csv_reader:
                if len(row) == 5:
                    line = {}
                    line["title"] = row[0]
                    line["from"] = row[1]
                    line["time"] = row[2]
                    line["question"] = row[3]
                    line["answer"] = row[4]
                    fqa_lines.append(line)
            fqa_lines.pop(0)
        function_logger.info("读取%s的常用问题集完成！" % university_name)
        function_logger.info("开始写入%s的常用问题集..." % university_name)
        with open(pickle_dir + "/" + university_name, "wb")as p_file:
            pickle.dump(fqa_lines, p_file)
        function_logger.info("写入%s的常用问题集完成！" % university_name)
    function_logger.info("数据处理完成！")


# 随机抽取数据，人工进行打分并放入相应的文件中
def label_data():
    function_logger = MyLog(logger=sys._getframe().f_code.co_name).getlog()
    data_dir = "Information/大学/常问问题集/Data"
    pickle_dir = "Information/大学/常问问题集/Pickle"
    label_dir = "Information/大学/常问问题集/label"
    file_list = os.listdir(pickle_dir)
    function_logger.debug("大学数量：%d" % len(file_list))
    line_1 = []
    line_2 = []
    line_3 = []
    line_4 = []
    line_5 = []
    line_6 = []
    line_7 = []
    all_count = 0
    for file in file_list:
        print(file)
        university_name = file
        with open(pickle_dir + "/" + university_name, "rb") as p_file:
            lines = pickle.load(p_file)
        lines_count = len(lines)
        all_count += lines_count
    print(all_count)
    #     group_size = 100
    #     for i_line in range(0, lines_count, 100):
    #         random_end = min(group_size, lines_count - i_line)
    #         random_index = random.randrange(0, random_end)
    #         print_line = lines[i_line + random_index]
    #         # print(print_line)
    #         print("\n%d/%d:\t%s" % (i_line+random_index,lines_count,print_line["question"]))
    #         print("0:不进行标记\t1:录取希望\t2:招生计划\t3:录取分数\t4:毕业去向\t5:专业相关\t6:谢谢回复\t7:志愿填报\t8:进行存储")
    #         print("标签数量：\t\t%6.d\t\t%6.d\t\t%6.d\t\t%6.d\t\t%6.d\t\t%6.d\t\t%6.d" %
    #               (len(line_1), len(line_2), len(line_3), len(line_4), len(line_5), len(line_6), len(line_7)))
    #         label = input("输入标签：")
    #         if label == "1":
    #             line_1.append(print_line)
    #         elif label == "2":
    #             line_2.append(print_line)
    #         elif label == "3":
    #             line_3.append(print_line)
    #         elif label == "4":
    #             line_4.append(print_line)
    #         elif label == "5":
    #             line_5.append(print_line)
    #         elif label == "6":
    #             line_6.append(print_line)
    #         elif label == "7":
    #             line_7.append(print_line)
    #         elif label == "8":
    #             with open(label_dir+"/admission_hope", "wb")as f:
    #                 f.truncate()
    #                 pickle.dump(line_1, f)
    # with open(label_dir+"/admission_hope", "w", encoding="utf-8") as f:
    #     f.truncate()
    #     pickle.dump(line_1, f)
        # function_logger.debug(university_name)


# 对数据进行处理，选出参与标注数据的文本
def brat_label_data():
    pickle_dir = "Information/大学/常问问题集/Pickle"
    brat_dir = "Information/大学/常问问题集/Brat"
    all_count = 0
    all_count_brat = 0
    all_count_else = 0
    file_list = os.listdir(pickle_dir)
    for i_file in range(len(file_list)):
        print(file_list[i_file])
        university_name = file_list[i_file]
        with open(pickle_dir + "/" + university_name, "rb") as p_file:
            lines = pickle.load(p_file)
        lines_count = len(lines)
        group_size = 100
        brat_index = []
        brat_datas = []
        all_count += lines_count
        for i_line in range(0, lines_count, 100):
            random_end = min(group_size, lines_count - i_line)
            random_index = random.randrange(0, random_end)
            brat_index.append(i_line+random_index)
        for i in brat_index:
            brat_datas.append(lines[i])
        all_count_brat += len(brat_datas)
        # 去除选出的数据
        for line in brat_datas:
            lines.remove(line)
        all_count_else += len(lines)
        with open(brat_dir+"/"+str(i_file)+".txt","w",encoding="utf-8") as f_bdata:
            for data in brat_datas:
                f_bdata.write(data["question"]+"\t"+data["answer"]+"\n")
        fp = open(brat_dir + "/" + str(i_file) + ".ann", "w")
        fp.close()
        with open(pickle_dir+"/"+university_name,"wb")as p_file:
            pickle.dump(lines, p_file)
    print(all_count)
    print(all_count_brat)
    print(all_count_else)


# 创建存储标注数据的文件.ann
def create_label_file():
    brat_dir = "Information/大学/常问问题集/Brat"
    for file in os.listdir(brat_dir):
        university_name = file[:-4]
        fp = open(brat_dir+"/"+university_name+".ann", "w")
        fp.close()
        print(university_name)

if __name__ == '__main__':
    main_logger = MyLog(__name__).getlog()
    main_logger.debug("start...")
    # get_undergraduate_university_info()
    # get_consultation_forum_id()
    # get_question_yggk()
    # pretreat_crawl_questions()

    # with open("Information/大学/university_info", "rb")as p_file:
    #     university_infos = pickle.load(p_file)
    # for info in university_infos:
    #     if "985" in info["院校特性"] and "211" in info["院校特性"]:
    #         print(info)

    # label_data()

    # pretreat_crawl_questions()

    # pickle_dir = "Information/大学/常问问题集/Pickle"
    # data_count = 0
    # for file in os.listdir(pickle_dir):
    #     print(file)
    #     with open(pickle_dir + "/" + file, "rb")as p_file:
    #         data = pickle.load(p_file)
    #     data_count+=len(data)
    #     for line in data:
    #         if len(line)!=5:
    #             print(line)
    # print("总记录数：%d" % data_count)

    # label_dir = "Information/大学/常问问题集/label"
    # with open(label_dir+"/admission_hope","rb") as p_file:
    #     data = pickle.load(p_file)
    # for line in data:
    #     print(line)

    brat_label_data()
    # create_label_file()

    main_logger.debug("end...")
