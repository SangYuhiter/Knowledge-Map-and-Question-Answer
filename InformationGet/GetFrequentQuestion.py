# -*- coding: utf-8 -*-
'''
@File  : GetFrequentQuestion.py
@Author: SangYu
@Date  : 2019/3/15 13:54
@Desc  : 获取常见问题集
'''
from bs4 import BeautifulSoup
from InformationGet.InternetConnect import request_url
from Log.Logger import MyLog
import sys
import time
import csv
import re


# 从阳光高考网获取常见问题集
def get_question_yggk():
    mylogger = MyLog(logger=sys._getframe().f_code.co_name).getlog()
    # 院校咨询页url
    main_url = "https://gaokao.chsi.com.cn"
    file_path = "Information/大学/Test"
    school_urls = [
        ["北京大学", str(26232)], ["哈尔滨工业大学", str(26617)], ["北京大学医学部", str(6405529)],
        ["上海交通大学", str(6217)], ["上海交通大学医学院", str(61811)], ["清华大学", str(36710)],
        ["复旦大学", str(7243)], ["南京大学", str(4453)], ["浙江大学", str(43617)], ["中国科学技术大学", str(6280)],
        ["哈尔滨工业大学(威海)", str(62646117)], ["西安交通大学", str(53593)]
    ]
    for school in school_urls:
        mylogger.info("开始抓取" + school[0] + "的招生问题数据...")
        # 创建该学校的问题集收集表,sheet,并写好表头
        table_head = ["标题", "来源", "时间", "问题", "回答"]
        with open(file_path + "/" + school[0] + "常用问题集.csv", "w",encoding='utf-8') as csvfile:
            csvfile.truncate()
            writer = csv.writer(csvfile)
            writer.writerow(table_head)
        main_page_source = request_url(
            "https://gaokao.chsi.com.cn/zxdy/forum--method-listDefault,year-2005,forumid-" + school[
                1] + ",start-0.dhtml")
        main_page_source.encoding = main_page_source.apparent_encoding
        main_page_soup = BeautifulSoup(main_page_source.content, "lxml")
        # 页面总数
        page_count = main_page_soup.find("li", class_="lip dot").next_sibling.a.string
        # 置顶问题个数
        top_question_count = len(main_page_soup.find("table", class_="ch-table zx-table")
                                 .find_all("span", class_="question_top_txt"))
        # 每页问题个数
        page_question_count = 15
        # 通过构造每一个页面url进入具体页面
        for i_page in list(range(10)) + list(range(11, int(page_count))):
            page_url = main_url + "/zxdy/forum--method-listDefault,year-2005,forumid-" + school[1] + ",start-" + str(
                i_page * page_question_count) + ".dhtml"
            # xls表格记录基点(页问题量+置顶问题量+表头)
            if i_page == 0:
                base_count = 1
            else:
                base_count = i_page * page_question_count + top_question_count + 1
            mylogger.info("页面抓取进度(%d,%d)" % (i_page + 1, int(page_count)))
            mylogger.info("页面url%s" % page_url)
            page_source = request_url(page_url)
            page_source.encoding = page_source.apparent_encoding
            page_soup = BeautifulSoup(page_source.text, "lxml")
            tr_list = page_soup.find("table", class_="ch-table zx-table").contents
            for item in tr_list:
                if item == "\n":
                    tr_list.remove(item)
            records = []
            # 置顶问答只记录一次
            if i_page == 0:
                start_index = 0
            else:
                start_index = top_question_count * 2
            for i_qa_pair in range(start_index, len(tr_list), 2):
                question_title = "q_title"
                question_from = ""
                question_time = ""
                question_text = "q_text"
                answer_text = "a_text"
                question_title = str(tr_list[i_qa_pair].find("a", class_="question_t_txt").string).strip()
                mylogger.debug("标题:%s" % question_title)
                question_from = str(tr_list[i_qa_pair].find("i", title="提问人").next_sibling.string).strip()
                mylogger.debug("来源:%s" % question_from)
                question_time = str(tr_list[i_qa_pair].find("td", class_="question_t ch-table-center").text).strip()
                mylogger.debug("时间:%s" % question_time)
                # 问题与答案可能出现本页无法写下的情况，需要进行页面跳转获取信息
                question_text_class = tr_list[i_qa_pair + 1].find("div", class_="question")
                if question_text_class.find(text='[详细]') is None:
                    question_text = str(question_text_class.text).strip()
                else:
                    turn_page_url = main_url + question_text_class.find("a", text='[详细]')["href"]
                    turn_page_source = request_url(turn_page_url)
                    turn_page_source.encoding = turn_page_source.apparent_encoding
                    turn_page_soup = BeautifulSoup(turn_page_source.text, "lxml")
                    question_text = str(turn_page_soup.find("div", class_="question").text).strip()
                mylogger.debug("问题:%s" % question_text)
                answer_text_class = tr_list[i_qa_pair + 1].find("div", class_="question_a")
                if answer_text_class.find(text='[详细]') is None:
                    answer_text = str(answer_text_class.text).replace("[ 回复 ]", "").strip()
                else:
                    turn_page_url = main_url + answer_text_class.find("a", text='[详细]')["href"]
                    turn_page_source = request_url(turn_page_url)
                    turn_page_source.encoding = turn_page_source.apparent_encoding
                    turn_page_soup = BeautifulSoup(turn_page_source.text, "lxml")
                    pattern = re.compile(r"\s+|\n|\t|\v|\ue63c")
                    answer_text = re.sub(pattern, "", str(turn_page_soup.find("div", class_="question_a").text))\
                        .replace("[回复]", "")
                mylogger.debug("回答:%s" % answer_text)
                records.append([question_title, question_from, question_time, question_text, answer_text])
            with open(file_path + "/" + school[0] + "常用问题集.csv", "a",encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                for record in records:
                    writer.writerow(record)
            time.sleep(3)
        mylogger.info("%s的常用问题集收集完毕！" % school[0])


if __name__ == '__main__':
    mylogger = MyLog(__name__).getlog()
    mylogger.debug("start...")
    get_question_yggk()
    mylogger.debug("end...")
