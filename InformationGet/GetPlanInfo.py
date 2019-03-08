#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File  : GetPlanInfo.py
@Author: SangYu
@Date  : 2018/12/21 12:38
@Desc  : 获取各学校招生计划信息
'''
import requests
from bs4 import BeautifulSoup
import re
from FileRead.FileNameRead import read_all_file_list
from FileRead.PDFRead import read_pdf_to_tables
from FileRead.XLSRead import read_xls
from InformationGet.InternetConnect import request_url, selenium_chrome
from Log.Logger import MyLog
from FileRead.ImageRead import image_to_pdf
import os
import sys

import pdfplumber


# 将表内容写入文本文件
def write_table(file_path, table_name, table_head, table_content):
    with open(file_path + "/" + table_name, 'w', encoding='utf-8') as file:
        for item in table_head:
            file.write(item + "\t")
        file.write("\n")
        for item in table_content:
            for sub_item in item:
                file.write(sub_item + "\t")
            file.write("\n")


# 哈尔滨工业大学招生计划
def get_plan_info_hit():
    mylogger = MyLog(logger=sys._getframe().f_code.co_name).getlog()
    mylogger.info("开始获取网页源码...")
    main_url = "http://zsb.hit.edu.cn/information/plan"
    # 获取分类信息
    main_page_source = requests.get(main_url).text
    main_page_soup = BeautifulSoup(main_page_source, "lxml")
    main_page_soup.prettify()
    # 招生计划省份
    mylogger.info("解析招生地区...")
    province = []
    for item in main_page_soup.find(class_="province").find_all(name='a'):
        province.append(item.string.strip())
    mylogger.debug("哈工大招生地区：" + str(province))
    # 招生计划年份
    mylogger.info("解析招生年份...")
    years = []
    for item in main_page_soup.find_all(class_="year-select"):
        years.append(item.string.strip())
    mylogger.debug("哈工大招生年份：" + str(years))

    # 对每年份各省数据进行抽取
    mylogger.info("开始获取各年各地区数据...")
    for pro in province:
        for year in years:
            mylogger.info("开始获取" + year + pro + "的招生计划")
            # 构造链接
            specific_url = main_url + "?" + "year=" + year + "&" + "province=" + pro
            page_source = requests.get(specific_url).text
            page_soup = BeautifulSoup(page_source, "lxml")
            page_soup.prettify()
            # 表名
            table_name = year + "-" + pro
            mylogger.debug("表名:" + table_name)
            # 表头
            table_head = []
            for item in page_soup.find(class_="info_table").thead.find_all(name="td"):
                table_head.append(item.string.strip())
            mylogger.debug("表头:" + str(table_head))
            # 表内容
            table_content = []
            for item in page_soup.find(class_="info_table").tbody.find_all(name="tr"):
                temp = []
                for sub_item in item.find_all(name="td"):
                    temp.append(sub_item.string.strip())
                table_content.append(temp)
            # 去除统计部分的数据项、无数据的项
            for item in table_content:
                if item[0] == "无数据":
                    table_content.remove(item)
                # elif item[1] == "统计":
                #     table_content.remove(item)
            mylogger.debug("表内容如下：")
            for item in table_content:
                mylogger.debug(item)
            # 将表内容写入文本文件
            file_path = "Information/九校联盟/哈尔滨工业大学/招生计划"
            write_table(file_path, table_name, table_head, table_content)
            mylogger.info(year + pro + "的招生计划已存入文件")


# 北京大学招生计划
def get_plan_info_pku():
    main_url = "http://www.gotopku.cn/programa/enrolstu/6.html"
    # 获取分类信息
    main_page_source = requests.get(main_url).text
    main_page_soup = BeautifulSoup(main_page_source, "lxml")
    main_page_soup.prettify()
    # 招生计划科别（文理）
    familes = []
    contents = main_page_soup.find(class_="lqlist").contents
    for item in contents[1].find_all(name='a'):
        familes.append(item.string.strip())
    print(familes)
    # 招生计划年份
    years = []
    for item in contents[3].find_all(name='a'):
        years.append(item.string.strip())
    print(years)
    # 招生计划地区
    district = []
    for item in main_page_soup.find(class_="kr").find_all(name='a'):
        district.append(item.string.strip())
    print(district)

    # 构造链接
    for year in years:
        for i_district in range(len(district)):
            table_content = []
            for i_families in range(len(familes)):
                new_main_url = "http://www.gotopku.cn/programa/enrolstu/6"
                specific_url = new_main_url + "/" + year + "/" + str(i_district + 1) + "/" + str(i_families) + ".html"
                page_source = requests.get(specific_url).text
                page_soup = BeautifulSoup(page_source, "lxml")
                page_soup.prettify()
                # 表名
                table_name = year + "-" + district[i_district]
                print("表名:", table_name)
                # 表内容(原表)
                source_table_content = []
                for item in page_soup.find(class_="lqtable").find_all(name="td"):
                    source_table_content.append(item.string.strip())
                # 表头
                table_head = source_table_content[:2]
                table_head.insert(1, "类别")
                print("表头:", table_head)
                source_table_content = source_table_content[4:]
                for i in range(0, len(source_table_content), 2):
                    temp = []
                    temp.append(source_table_content[i])
                    if i_families == 0:
                        temp.append("文史")
                    else:
                        temp.append("理工")
                    temp.append(source_table_content[i + 1])
                    table_content.append(temp)
                for item in table_content:
                    print(item)
            # 将表内容写入文本文件
            file_path = "Information/九校联盟/北京大学/招生计划"
            write_table(file_path, table_name, table_head, table_content)


# 北大医学部招生计划数据(2017\2016计划,2015无数据)
def get_plan_info_pkuhsc():
    get_plan_info_pkuhsc_2017()
    get_plan_info_pkuhsc_2016()


# 北大医学部招生计划数据2017
def get_plan_info_pkuhsc_2017():
    main_url = "http://jiaoyuchu.bjmu.edu.cn/zsjy/zsgz/zsjh"
    year = "2017"
    # 构造链接
    specific_url = main_url + "/" + year + "/"
    print(specific_url)
    page_source = requests.get(specific_url)
    page_source.encoding = "utf-8"
    page_soup = BeautifulSoup(page_source.text, "lxml")
    page_soup.prettify()
    year_and_district = page_soup.find_all(class_="link_new01")
    district = []
    district_url = []
    for item in year_and_district[1].find_all(name='a'):
        district.append(item.string.strip())
        district_url.append(item['href'])
    print(district)
    print(district_url)
    for i_url in range(len(district_url)):
        if district[i_url] == "新疆预科" or district[i_url] == "内蒙古预科" or district[i_url] == "新疆西藏内地班":
            break
        table_source = requests.get(specific_url + district_url[i_url])
        table_source.encoding = "utf-8"
        table_soup = BeautifulSoup(table_source.text, "lxml")
        table_soup.prettify()
        table_content = []
        for item in table_soup.find(class_="box_new02").table.tbody.find_all(name="tr"):
            temp = []
            for sub_item in item.find_all(name="td"):
                temp.append(sub_item.text.strip())
                # print(sub_item.text.strip())
            temp.pop(0)
            table_content.append(temp)
        table_name = year + "-" + district[i_url]
        table_head = table_content[0]
        table_head[1] = "类别"
        table_content = table_content[1:]
        for i in range(len(table_content)):
            table_content[i][0] += table_content[i][1] + "年"
            table_content[i][1] = "医科"
        print(table_name)
        print(table_head)
        for item in table_content:
            print(item)
        file_path = "Information/九校联盟/北京大学医学部/招生计划"
        write_table(file_path, table_name, table_head, table_content)


# 北大医学部招生计划数据2016
def get_plan_info_pkuhsc_2016():
    main_url = "http://jiaoyuchu.bjmu.edu.cn/zsjy/zsgz/zsjh"
    year = "2016"
    # 构造链接
    specific_url = main_url + "/" + year + "/"
    # print(specific_url)
    page_source = requests.get(specific_url)
    page_source.encoding = "utf-8"
    page_soup = BeautifulSoup(page_source.text, "lxml")
    page_soup.prettify()
    year_and_district = page_soup.find_all(class_="link_new01")
    district = []
    district_url = []
    for item in year_and_district[1].find_all(name='a'):
        district.append(item.string.strip())
        district_url.append(item['href'])
    print(district)
    print(district_url)
    for i_url in range(len(district_url)):
        if district[i_url] == "新疆预科" or district[i_url] == "内蒙古预科" or district[i_url] == "新疆西藏内地班":
            break
        table_source = requests.get(specific_url + district_url[i_url])
        table_source.encoding = "utf-8"
        table_soup = BeautifulSoup(table_source.text, "lxml")
        table_soup.prettify()
        table_content = []
        for item in table_soup.find(class_="box_new02").table.tbody.find_all(name="tr"):
            temp = []
            for sub_item in item.find_all(name="td"):
                temp.append(sub_item.text.strip())
                # print(sub_item.text.strip())
            table_content.append(temp)
        table_name = year + "-" + district[i_url]
        table_head = table_content[0]
        table_head[1] = "类别"
        table_content = table_content[1:]
        for i in range(len(table_content)):
            table_content[i][0] += table_content[i][1] + "年"
            table_content[i][1] = "医科"
        print(table_name)
        print(table_head)
        for item in table_content:
            print(item)
        file_path = "Information/九校联盟/北京大学医学部/招生计划"
        write_table(file_path, table_name, table_head, table_content)


# 清华大学招生计划
def get_plan_info_tsinghua():
    main_url = "http://www.join-tsinghua.edu.cn"
    url = main_url + "/publish/bzw/7540/index.html"
    page_source = requests.get(url)
    page_source.encoding = page_source.apparent_encoding
    page_soup = BeautifulSoup(page_source.text, "lxml")
    page_soup.prettify()
    main_file_path = "Information/九校联盟/清华大学/招生计划"
    # 下载文件
    print("开始下载文件")
    for item in page_soup.find("ul", class_="ulList").find_all("li"):
        if item.a["title"].find("计划") == -1:
            continue
        specific_url = main_url + item.a["href"]
        sub_page_source = requests.get(specific_url)
        sub_page_source.encoding = "utf-8"
        sub_page_soup = BeautifulSoup(sub_page_source.text, "lxml")
        sub_page_soup.prettify()
        file_name = sub_page_soup.find("a", text=re.compile("附件|xls")).text
        if file_name.find(".") == -1:
            file_name += ".pdf"
        file_url = sub_page_soup.find("a", text=re.compile("附件|xls"))["href"]
        file_content = requests.get(main_url + file_url)
        with open(main_file_path + "/source/" + file_name, "wb") as pdf:
            pdf.write(file_content.content)
    print("文件下载完成！")

    # 文件解析
    print("开始文件解析")
    file_list = read_all_file_list(main_file_path + "/source")
    file_2010 = []
    file_2009 = []
    for item in file_list:
        if item[-3:] == "pdf":
            if item.find("2014") != -1:
                write_plan_info_tsinghua_2014(main_file_path, item)
                print("2014年数据解析完成！")
            if item.find("2013") != -1:
                write_plan_info_tsinghua_2013(main_file_path, item)
                print("2013年数据解析完成！")
        if item[-3:] == "xls":
            if item.find("2012") != -1:
                write_plan_info_tsinghua_2012(main_file_path, item)
                print("2012年数据解析完成！")
            if item.find("2011") != -1:
                write_plan_info_tsinghua_2011(main_file_path, item)
                print("2011年数据解析完成！")
            if item.find("2010") != -1:
                file_2010.append(item)
            if item.find("2009") != -1:
                file_2009.append(item)
    # 2010,2009有多个文件，传入文件列表
    write_plan_info_tsinghua_2010(main_file_path, file_2010)
    print("2010年数据解析完成！")
    write_plan_info_tsinghua_2009(main_file_path, file_2009)
    print("2009年数据解析完成！")


# 清华大学招生计划数据2014
def write_plan_info_tsinghua_2014(store_path, info_path):
    year = "2014"
    pages = read_pdf_to_tables(info_path)
    li_table = pages[0][0] + pages[1][0]
    wen_table = pages[1][1]
    # 理科
    table_head = li_table[0]
    for i in range(len(table_head)):
        table_head[i] = table_head[i].replace("\n", "")
    pro_line_li = li_table[-1]
    pro_line_wen = wen_table[-1]
    for item in li_table:
        if item[0] == "专业名称" or item[0] == "理科合计":
            li_table.remove(item)
    for item in wen_table:
        if item[0] == "专业名称" or item[0] == "文科合计":
            wen_table.remove(item)

    # 写入文件
    for i_pro in range(1, len(table_head)):
        sub_plan_table_name = year + "-" + table_head[i_pro]
        sub_plan_table_head = ["专业", "类别", "人数"]
        sub_plan_table_content = []
        # 理科部分
        for item in li_table:
            if item[i_pro] != "":
                temp = [item[0].replace("\n", ""), "理工", item[i_pro]]
                sub_plan_table_content.append(temp)
        # 统计人数
        temp = ["理工", "统计", pro_line_li[i_pro]]
        sub_plan_table_content.append(temp)
        # 文科部分
        for item in wen_table:
            if item[i_pro] != "":
                temp = [item[0], "文史", item[i_pro]]
                sub_plan_table_content.append(temp)
        # 统计人数
        temp = ["文史", "统计", pro_line_wen[i_pro]]
        sub_plan_table_content.append(temp)

        write_table(store_path, sub_plan_table_name, sub_plan_table_head, sub_plan_table_content)
        # print(sub_plan_table_name)
        # print(sub_plan_table_head)
        # for item in sub_plan_table_content:
        #     print(item)


# 清华大学招生计划数据2013
def write_plan_info_tsinghua_2013(store_path, info_path):
    year = "2013"
    pages = read_pdf_to_tables(info_path)
    li_table = pages[0][0]
    index = 0
    for i_line in range(len(pages[1][0])):
        if pages[1][0][i_line][0] == "专业名称":
            index = i_line
            break
    li_table += pages[1][0][:index]
    wen_table = pages[1][0][index:]
    li_table = li_table[1:-1]
    wen_table = wen_table[:-1]

    # 理科
    table_head = li_table[0]
    for i in range(len(table_head)):
        table_head[i] = table_head[i].replace("\n", "")
        if table_head[i] == "黑龙":
            table_head[i] = "黑龙江"
        if table_head[i] == "内蒙":
            table_head[i] = "内蒙古"
    pro_line_li = li_table[-1]
    pro_line_wen = wen_table[-1]
    for item in li_table:
        if item[0] == "专业名称" or item[0] == "理科合计":
            li_table.remove(item)
    for item in wen_table:
        if item[0] == "专业名称" or item[0] == "文科合计":
            wen_table.remove(item)
    # print(table_head)
    # for item in li_table:
    #     print(item)
    # print("---------------")
    # for item in wen_table:
    #     print(item)
    # 写入文件
    for i_pro in range(2, len(table_head)):
        sub_plan_table_name = year + "-" + table_head[i_pro]
        sub_plan_table_head = ["专业", "类别", "人数"]
        sub_plan_table_content = []
        # 理科部分
        for item in li_table:
            if item[i_pro] != "":
                temp = [item[0], "理工", item[i_pro]]
                sub_plan_table_content.append(temp)
        # 统计人数
        temp = ["理工", "统计", pro_line_li[i_pro]]
        sub_plan_table_content.append(temp)
        # 文科部分
        for item in wen_table:
            if item[i_pro] != "":
                temp = [item[0], "文史", item[i_pro]]
                sub_plan_table_content.append(temp)
        # 统计人数
        temp = ["文史", "统计", pro_line_wen[i_pro]]
        sub_plan_table_content.append(temp)

        write_table(store_path, sub_plan_table_name, sub_plan_table_head, sub_plan_table_content)
        # print(sub_plan_table_name)
        # print(sub_plan_table_head)
        # for item in sub_plan_table_content:
        #     print(item)


# 清华大学招生计划数据2012
def write_plan_info_tsinghua_2012(store_path, info_path):
    year = "2012"
    excel_file = read_xls(info_path)
    # 理科
    sheet_names = excel_file.sheet_names()
    sheet_li = excel_file.sheet_by_name(sheet_names[0])
    sheet_wen = excel_file.sheet_by_name(sheet_names[1])
    li_table = []
    wen_table = []
    for i_row in range(sheet_li.nrows):
        li_table.append(sheet_li.row_values(i_row))
    for i_row in range(sheet_wen.nrows):
        wen_table.append(sheet_wen.row_values(i_row))
    li_table = [li_table[1]] + li_table[3:-3]
    wen_table = [wen_table[1]] + wen_table[3:-3]

    # 理科
    table_head = li_table[0]
    pro_line_li = li_table[-1]
    pro_line_wen = wen_table[-1]
    for item in li_table:
        if item[0] == "专业名称" or item[0] == "合计":
            li_table.remove(item)
    for item in wen_table:
        if item[0] == "专业名称" or item[0] == "合计":
            wen_table.remove(item)
    # for item in li_table:
    #     print(item)
    # print("---------------")
    # for item in wen_table:
    #     print(item)
    # 写入文件
    for i_pro in range(1, len(table_head)):
        sub_plan_table_name = year + "-" + table_head[i_pro]
        sub_plan_table_head = ["专业", "类别", "人数"]
        sub_plan_table_content = []
        # 理科部分
        for item in li_table:
            if item[i_pro] != "":
                temp = [item[0], "理工", str(int(item[i_pro]))]
                sub_plan_table_content.append(temp)
        # 统计人数
        temp = ["理工", "统计", str(int(pro_line_li[i_pro]))]
        sub_plan_table_content.append(temp)
        # 文科部分
        for item in wen_table:
            if item[i_pro] != "":
                temp = [item[0], "文史", str(int(item[i_pro]))]
                sub_plan_table_content.append(temp)
        # 统计人数
        temp = ["文史", "统计", str(int(pro_line_wen[i_pro]))]
        sub_plan_table_content.append(temp)

        write_table(store_path, sub_plan_table_name, sub_plan_table_head, sub_plan_table_content)
        # print(sub_plan_table_name)
        # print(sub_plan_table_head)
        # for item in sub_plan_table_content:
        #     print(item)


# 清华大学招生计划数据2011
def write_plan_info_tsinghua_2011(store_path, info_path):
    year = "2011"
    excel_file = read_xls(info_path)
    # 理科
    sheet_names = excel_file.sheet_names()
    sheet_li = excel_file.sheet_by_name(sheet_names[0])
    sheet_wen = excel_file.sheet_by_name(sheet_names[1])
    li_table = []
    wen_table = []
    for i_row in range(sheet_li.nrows):
        li_table.append(sheet_li.row_values(i_row))
    for i_row in range(sheet_wen.nrows):
        wen_table.append(sheet_wen.row_values(i_row))
    li_table = [li_table[1]] + li_table[3:-5]
    wen_table = [wen_table[1]] + wen_table[3:-5]

    # 理科
    table_head = li_table[0]
    pro_line_li = li_table[-1]
    pro_line_wen = wen_table[-1]
    for item in li_table:
        if item[0] == "专业名称" or item[0] == "合计":
            li_table.remove(item)
    for item in wen_table:
        if item[0] == "专业名称" or item[0] == "合计":
            wen_table.remove(item)
    # for item in li_table:
    #     print(item)
    # print("---------------")
    # for item in wen_table:
    #     print(item)
    # 写入文件
    for i_pro in range(1, len(table_head)):
        sub_plan_table_name = year + "-" + table_head[i_pro]
        sub_plan_table_head = ["专业", "类别", "人数"]
        sub_plan_table_content = []
        # 理科部分
        for item in li_table:
            if item[i_pro] != "":
                temp = [item[0], "理工", str(int(item[i_pro]))]
                sub_plan_table_content.append(temp)
        # 统计人数
        temp = ["理工", "统计", str(int(pro_line_li[i_pro]))]
        sub_plan_table_content.append(temp)
        # 文科部分
        for item in wen_table:
            if item[i_pro] != "":
                temp = [item[0], "文史", str(int(item[i_pro]))]
                sub_plan_table_content.append(temp)
        # 统计人数
        temp = ["文史", "统计", str(int(pro_line_wen[i_pro]))]
        sub_plan_table_content.append(temp)

        write_table(store_path, sub_plan_table_name, sub_plan_table_head, sub_plan_table_content)
        # print(sub_plan_table_name)
        # print(sub_plan_table_head)
        # for item in sub_plan_table_content:
        #     print(item)


# 清华大学招生计划数据2010
def write_plan_info_tsinghua_2010(store_path, info_path_list):
    year = "2010"
    li_table = []
    wen_table = []
    for info_path in info_path_list:
        excel_file = read_xls(info_path)
        flag = info_path.find("理工")
        sheet = excel_file.sheet_by_index(0)
        # 理科
        if flag != -1:
            for i_row in range(sheet.nrows):
                li_table.append(sheet.row_values(i_row))
        else:
            for i_row in range(sheet.nrows):
                wen_table.append(sheet.row_values(i_row))
    index = 0
    for i_line in range(len(li_table)):
        if li_table[i_line][0] == "专业名称":
            index = i_line
    pro_line_li_1 = li_table[3]
    pro_line_li_2 = li_table[index + 2]
    pro_line_wen = wen_table[3]
    table_head = li_table[index]
    li_table = li_table[4:index - 3] + li_table[index + 3:-5]
    wen_table = wen_table[4:-7]
    # for item in li_table:
    #     print(item)
    # print("---------------")
    # for item in wen_table:
    #     print(item)

    # 写入文件
    for i_pro in range(1, len(table_head)):
        sub_plan_table_name = year + "-" + table_head[i_pro]
        sub_plan_table_head = ["专业", "类别", "人数"]
        sub_plan_table_content = []
        # 理科部分
        for item in li_table:
            if item[i_pro] != "":
                temp = [item[0], "理工", str(int(item[i_pro]))]
                sub_plan_table_content.append(temp)
        # 统计人数
        temp = ["理工", "统计", str(int(pro_line_li_1[i_pro] + pro_line_li_2[i_pro]))]
        sub_plan_table_content.append(temp)
        # 文科部分
        for item in wen_table:
            if item[i_pro] != "":
                temp = [item[0], "文史", str(int(item[i_pro]))]
                sub_plan_table_content.append(temp)
        # 统计人数
        temp = ["文史", "统计", str(int(pro_line_wen[i_pro]))]
        sub_plan_table_content.append(temp)

        write_table(store_path, sub_plan_table_name, sub_plan_table_head, sub_plan_table_content)
        # print(sub_plan_table_name)
        # print(sub_plan_table_head)
        # for item in sub_plan_table_content:
        #     print(item)


# 清华大学招生计划数据2009
def write_plan_info_tsinghua_2009(store_path, info_path_list):
    year = "2009"
    li_table = []
    wen_table = []
    for info_path in info_path_list:
        excel_file = read_xls(info_path)
        flag = info_path.find("理工")
        sheet = excel_file.sheet_by_index(0)
        # 理科
        if flag != -1:
            for i_row in range(sheet.nrows):
                li_table.append(sheet.row_values(i_row)[:-1])
            sheet_add_li = excel_file.sheet_by_index(1)
            for i_row in range(sheet_add_li.nrows):
                li_table.append(sheet_add_li.row_values(i_row)[:-1])
        else:
            for i_row in range(sheet.nrows):
                wen_table.append(sheet.row_values(i_row)[:-1])
    index = 0
    for i_line in range(len(li_table)):
        if li_table[i_line][0] == "2009合计":
            index = i_line
    pro_line_li_1 = li_table[3]
    pro_line_li_2 = li_table[index]
    pro_line_wen = wen_table[3]
    table_head = li_table[1]
    li_table = li_table[4:index - 12] + li_table[index + 1:-30]
    wen_table = wen_table[4:-8]
    # for item in li_table:
    #     print(item)
    # print("---------------")
    # for item in wen_table:
    #     print(item)

    # 写入文件
    for i_pro in range(1, len(table_head)):
        sub_plan_table_name = year + "-" + table_head[i_pro]
        sub_plan_table_head = ["专业", "类别", "人数"]
        sub_plan_table_content = []
        # 理科部分
        for item in li_table:
            if item[i_pro] != "":
                temp = [item[0], "理工", str(int(item[i_pro]))]
                sub_plan_table_content.append(temp)
        # 统计人数
        temp = ["理工", "统计", str(int(pro_line_li_1[i_pro] + pro_line_li_2[i_pro]))]
        sub_plan_table_content.append(temp)
        # 文科部分
        for item in wen_table:
            if item[i_pro] != "":
                temp = [item[0], "文史", str(int(item[i_pro]))]
                sub_plan_table_content.append(temp)
        # 统计人数
        temp = ["文史", "统计", str(int(pro_line_wen[i_pro]))]
        sub_plan_table_content.append(temp)

        write_table(store_path, sub_plan_table_name, sub_plan_table_head, sub_plan_table_content)
        # print(sub_plan_table_name)
        # print(sub_plan_table_head)
        # for item in sub_plan_table_content:
        #     print(item)


# 上海交通大学招生计划
def get_plan_info_sjtu():
    mylogger = MyLog(logger=sys._getframe().f_code.co_name).getlog()
    # main_url = "http://zsb.sjtu.edu.cn/web/jdzsb"
    # url = main_url + "/3810061.htm"
    # page_source = request_url(url)
    # page_source.encoding = page_source.apparent_encoding
    # page_soup = BeautifulSoup(page_source.text, "lxml")
    # page_soup.prettify()
    main_file_path = "Information/九校联盟/上海交通大学/招生计划"
    # 下载文件
    # logger.info("开始下载文件")
    # for item in page_soup.find("ul", class_="infor_right02_cont").find_all("li"):
    #     logger.debug(item.a["title"])
    #     logger.debug(re.findall('\d{4}', item.a["title"]))
    #     year = re.findall('\d{4}', item.a["title"])[0]
    #     logger.debug(item.a["href"])
    #     specific_url = main_url + "/" + item.a["href"]
    #     sub_page_source = request_url(specific_url)
    #     sub_page_source.encoding = "utf-8"
    #     sub_page_soup = BeautifulSoup(sub_page_source.text, "lxml")
    #     sub_page_soup.prettify()
    #     image_index = 0
    #     for sub_item in sub_page_soup.find("div", class_="artical_box").find_all("img"):
    #         file_name = year + str(image_index) + sub_item["src"].split("/")[-1][-4:]
    #         file_url = sub_item["src"]
    #         if file_url[0] == "f":
    #             continue
    #         else:
    #             file_content = request_url("http://zsb.sjtu.edu.cn" + file_url)
    #         with open(main_file_path + "/source/" + file_name, "wb") as img:
    #             img.write(file_content.content)
    #         image_index += 1
    # logger.info("文件下载完成！")

    # 文件解析
    # logger.info("开始文件解析")
    # file_list = read_all_file_list(main_file_path + "/source")
    # file_2015 = []
    # file_2016 = []
    # file_2017 = []
    # file_2018 = []
    # for item in file_list:
    #     if item[-3:] == "jpg" or item[-3:] == "png":
    #         if item.find("2015") != -1:
    #             file_2015.append(item)
    #         elif item.find("2016") != -1:
    #             file_2016.append(item)
    #         elif item.find("2017") != -1:
    #             file_2017.append(item)
    #         elif item.find("2018") != -1:
    #             file_2018.append(item)
    # logger.info("图片文件转为pdf文件")
    # store_path = os.getcwd() + "/" + main_file_path + "/source"
    # image_to_pdf(file_2015, store_path, "2015.pdf")
    # image_to_pdf(file_2016, store_path, "2016.pdf")
    # image_to_pdf(file_2017, store_path, "2017.pdf")
    # image_to_pdf(file_2018, store_path, "2018.pdf")
    # logger.info("图片文件转成pdf完成！")
    # 重新读入文件列表
    file_list = read_all_file_list(main_file_path + "/source")
    for item in file_list:
        if item[-3:] == "pdf":
            if item.find("2015") != -1:
                # write_plan_info_sjtu_2015(main_file_path, item)
                mylogger.info("2015年数据解析完成！")
            elif item.find("2016") != -1:
                # write_plan_info_sjtu_2016(main_file_path, item)
                mylogger.info("2016年数据解析完成！")
            elif item.find("2017") != -1:
                # write_plan_info_sjtu_2017(main_file_path, item)
                mylogger.info("2017年数据解析完成！")
            elif item.find("2018") != -1:
                # write_plan_info_sjtu_2018(main_file_path, item)
                mylogger.info("2018年数据解析完成！")
            print(item)


# 上海交通大学招生计划数据2018
def write_plan_info_sjtu_2018(store_path, info_path):
    mylogger = MyLog(logger=sys._getframe().f_code.co_name).getlog()
    info_path = "Information/九校联盟/上海交通大学/招生计划/source/2018test.pdf"
    year = "2018"
    # pages = read_pdf_to_tables(info_path)
    with pdfplumber.open(info_path) as pdf:
        for page in [pdf.pages[0]]:
            print(len(page.extract_tables()))

    # for page in pages:
    #     for table in page:
    #         print(table)
    # li_table = pages[0][0] + pages[1][0]
    # wen_table = pages[1][1]
    # # 理科
    # table_head = li_table[0]
    # for i in range(len(table_head)):
    #     table_head[i] = table_head[i].replace("\n", "")
    # pro_line_li = li_table[-1]
    # pro_line_wen = wen_table[-1]
    # for item in li_table:
    #     if item[0] == "专业名称" or item[0] == "理科合计":
    #         li_table.remove(item)
    # for item in wen_table:
    #     if item[0] == "专业名称" or item[0] == "文科合计":
    #         wen_table.remove(item)
    #
    # # 写入文件
    # for i_pro in range(1, len(table_head)):
    #     sub_plan_table_name = year + "-" + table_head[i_pro]
    #     sub_plan_table_head = ["专业", "类别", "人数"]
    #     sub_plan_table_content = []
    #     # 理科部分
    #     for item in li_table:
    #         if item[i_pro] != "":
    #             temp = [item[0].replace("\n", ""), "理工", item[i_pro]]
    #             sub_plan_table_content.append(temp)
    #     # 统计人数
    #     temp = ["理工", "统计", pro_line_li[i_pro]]
    #     sub_plan_table_content.append(temp)
    #     # 文科部分
    #     for item in wen_table:
    #         if item[i_pro] != "":
    #             temp = [item[0], "文史", item[i_pro]]
    #             sub_plan_table_content.append(temp)
    #     # 统计人数
    #     temp = ["文史", "统计", pro_line_wen[i_pro]]
    #     sub_plan_table_content.append(temp)
    #
    #     write_table(store_path, sub_plan_table_name, sub_plan_table_head, sub_plan_table_content)
    #     # print(sub_plan_table_name)
    #     # print(sub_plan_table_head)
    #     # for item in sub_plan_table_content:
    #     #     print(item)


# 上海交通大学招生计划数据2017
def write_plan_info_sjtu_2017(store_path, info_path):
    print("2017")


# 上海交通大学招生计划数据2016
def write_plan_info_sjtu_2016(store_path, info_path):
    print("2016")


# 上海交通大学招生计划数据2015
def write_plan_info_sjtu_2015(store_path, info_path):
    print("2015")


# 南京大学招生计划数据
def get_plan_info_nju():
    mylogger = MyLog(logger=sys._getframe().f_code.co_name).getlog()
    mylogger.info("开始获取网页源码...")
    main_url = "http://bkzs.nju.edu.cn"
    # 获取分类信息

    file_path = "Information/九校联盟/南京大学/招生计划"
    # 使用selenium获取隐藏部分源码
    # browser = selenium_chrome(main_url+"/4543/list.htm")
    # pro_list = browser.find_element_by_id("MapControl")
    # with open(file_path+"/source/"+"index","w",encoding="utf-8") as file:
    #     file.write(pro_list.get_attribute('innerHTML'))
    # 开始将源码读入并使用bs4解析
    with open(file_path + "/source/" + "index", "r", encoding="utf-8") as file:
        source_code = file.read()
    main_page_soup = BeautifulSoup(source_code, "lxml")
    main_page_soup.prettify()
    for li in [main_page_soup.find_all("li")[0]]:
        url = li.a["href"]
        pro = li.span.text
        print(pro + "\t" + url)
        page_source = request_url(main_url + url)
        page_soup = BeautifulSoup(page_source.text, "lxml")
        print(page_soup.find("div", class_="flexpaper_page"))
        # browser = selenium_chrome(main_url+url)
        # page_source = browser.find_element_by_class_name("flexpaper_page").find_element_by_tag_name("img")
        # print(page_source.text)
        # browser.quit()
        # img_url = page_soup.find_all("img")[0]["src"]
        # print(page_soup.find_all("img")[0]["src"])
        # img_source = request_url(main_url+img_url)
        # with open(file_path+"/source/"+"2018-"+ pro+".png","wb") as img:
        #     img.write(img_source.content)

    # # Ajax渲染，form方法获取json数据
    # params = {"siteId": "249",
    #             "columnId": "4543",
    #             "pageIndex": "1",
    #             "orders": "[]",
    #           "returnInfos": [{"field": "title", "pattern": [{"name": "lp", "value": "30"}], "name": "title"},
    #                         {"field": "shortTitle", "name": "shortTitle"}, {"field": "subTitle", "name": "subTitle"},
    #                         {"field": "publishTime", "pattern": [{"name": "d", "value": "yyyy-MM-dd hh:mm:ss"}],
    #                          "name": "publishTime"},
    #                         {"field": "createTime", "pattern": [{"name": "d", "value": "yyyy-MM-dd hh:mm:ss"}],
    #                          "name": "createTime"},
    #                         {"field": "summary", "pattern": [{"name": "lp", "value": "100"}], "name": "summary"}]}
    # html = requests.post("http://bkzs.nju.edu.cn/_wp3services/generalQuery?queryObj=articles",data=params)
    # print(html.text)


# 西安交通大学录取分数
def get_plan_info_xjtu():
    mylogger = MyLog(logger=sys._getframe().f_code.co_name).getlog()
    file_path = "Information/九校联盟/西安交通大学/招生计划"
    # 通过获取单个网页获取信息，需要后续处理，很麻烦
    """
    mylogger.info("开始获取网页源码...共五个网页")
    with open(file_path+"/source/page_url_list","w",encoding="utf-8")as url_file:
        for i in range(1, 6):
            main_url = "http://zs.xjtu.edu.cn/lmy.jsp?a43639t=5&a43639p=" + str(i) \
                       + "&a43639c=10&urltype=tree.TreeTempUrl&wbtreeid=1005"
            # 获取分类信息
            main_page_source = requests.get(main_url).text
            main_page_soup = BeautifulSoup(main_page_source, "lxml")
            main_page_soup.prettify()
            for item in main_page_soup.find("div", id="fybt").find("ul").find_all("a"):
                url_file.write(str(item)+"\n")
    mylogger.info("招生计划页面url获取完成")
    mylogger.info("开始获取具体页面信息")
    with open(file_path + "/source/page_url_list", "r", encoding="utf-8")as url_file:
        url_source = url_file.read()
    url_soup = BeautifulSoup(url_source,"lxml")
    url_soup.prettify()
    for page_url in url_soup.find_all("a"):
        print(page_url)
    """

    # 直接从官网进行数据查询，使用form提交
    # 获取可查询的年份和地区
    main_url = "http://zs.xjtu.edu.cn/bkscx/zsjhcx.htm"
    main_page_source = request_url(main_url)
    main_page_source.encoding = main_page_source.apparent_encoding
    main_page_soup = BeautifulSoup(main_page_source.text, "lxml")
    main_page_soup.prettify()
    years = []
    districts = []
    for year in main_page_soup.find("select",id="nf").find_all("option"):
        years.append(year.string)
    for district in main_page_soup.find("select",id="sf").find_all("option")[1:]:
        districts.append(district.string)
    mylogger.debug("可查询的年份"+str(years))
    mylogger.debug("可查询的省份" + str(districts))

    search_url = "http://zs.xjtu.edu.cn/zsjg.jsp?wbtreeid=1168"
    for year in years:
        for district in districts:
            # x,y 是查询按钮点击时的坐标，查询按钮大小x,y(54x22)
            params = {
                "nf":year,
                "sf":district,
                "x":"27",
                "y":"11"
            }
            return_html = requests.post(search_url,data=params)
            return_soup = BeautifulSoup(return_html.text,"lxml")
            return_soup.prettify()
            all_lines = []
            for tr in return_soup.find("div",id="fybt").find_all("tr"):
                line = []
                for td in tr:
                    if td.string != "\n":
                        line.append(str(td.string).strip())
                all_lines.append(line)
            table_name = year+"-"+district[:-1]
            table_head = ["专业","类别","人数"]
            table_content = []
            for line in all_lines[1:-1]:
                classy = line[2]
                if classy=="理":
                    classy = "理工"
                if classy == "文":
                    classy = "文史"
                table_content.append([line[0],classy,line[4]])
            mylogger.debug(table_name)
            mylogger.debug(str(table_head))
            for line in table_content:
                mylogger.debug(str(line))
            write_table(file_path, table_name, table_head, table_content)
            mylogger.info(year + district + "的招生计划已存入文件")



# 浙江大学录取分数
# 中国科学技术大学录取分数
# 复旦大学录取分数


if __name__ == "__main__":
    mylogger = MyLog(logger=__name__).getlog()
    mylogger.info("start...")
    # get_plan_info_hit()
    # get_plan_info_pku()
    # get_plan_info_pkuhsc()
    # get_plan_info_tsinghua()
    # 上交未完成，不可使用，bug多
    # get_plan_info_sjtu()
    # 南京大学未完成
    # get_plan_info_nju()
    get_plan_info_xjtu()
    mylogger.info("end...")
