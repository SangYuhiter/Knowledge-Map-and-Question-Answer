#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File  : GetScoreInfo.py
@Author: SangYu
@Date  : 2018/12/25 9:45
@Desc  : 获取各学校录取分数信息
'''

import requests
from bs4 import BeautifulSoup
import re
from FileRead.FileNameRead import read_all_file_list
from FileRead.XLSRead import read_xls
from FileRead.PDFRead import read_pdf_to_tables


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


# 哈尔滨工业大学录取分数
def get_score_info_hit():
    main_url = "http://zsb.hit.edu.cn/information/score"
    # 获取分类信息
    main_page_source = requests.get(main_url).text
    main_page_soup = BeautifulSoup(main_page_source, "lxml")
    main_page_soup.prettify()
    # 招生计划省份
    province = []
    for item in main_page_soup.find(class_="province").find_all(name='a'):
        province.append(item.string.strip())
    # print(province)
    # 招生计划年份
    years = []
    for item in main_page_soup.find_all(class_="year-select"):
        years.append(item.string.strip())
    # print(years)

    # 对每年份各省数据进行抽取
    for pro in province:
        for year in years:
            print("获取", year, pro, "的录取分数")
            # 构造链接
            specific_url = main_url + "?" + "year=" + year + "&" + "province=" + pro
            page_source = requests.get(specific_url).text
            page_soup = BeautifulSoup(page_source, "lxml")
            page_soup.prettify()
            # 表名
            table_name = year + "-" + pro + "-" + "major"
            print("表名:", table_name)
            # 表头
            table_head = []
            for item in page_soup.find(class_="info_table").thead.find_all(name="td"):
                table_head.append(item.string.strip())
            print("表头:", table_head)
            # 表内容
            table_content = []
            for item in page_soup.find(class_="info_table").tbody.find_all(name="tr"):
                temp = []
                for sub_item in item.find_all(name="td"):
                    temp.append(sub_item.string.strip())
                table_content.append(temp)
            # 去除统计部分的数据项、无数据的项
            for item in table_content:
                if item[1] == "统计":
                    table_content.remove(item)
            for item in table_content:
                print(item)
            # 将表内容写入文本文件
            file_path = "Information/九校联盟/哈尔滨工业大学/录取分数"
            write_table(file_path, table_name, table_head, table_content)
            print(year, pro, "的录取分数已存入文件")


# 北京大学录取分数(省份录取信息，没有专业分数)
def get_score_info_pku():
    main_url = "http://www.gotopku.cn/programa/admitline/7"
    # 获取分类信息
    main_page_source = requests.get(main_url).text
    main_page_soup = BeautifulSoup(main_page_source, "lxml")
    main_page_soup.prettify()
    # 招生计划年份
    years = []
    for item in main_page_soup.find(class_="lqlist").find_all(name='a'):
        years.append(item.string.strip())
    print(years)

    for year in years:
        # 构造链接
        specific_url = main_url + "/" + year
        page_source = requests.get(specific_url).text
        page_soup = BeautifulSoup(page_source, "lxml")
        page_soup.prettify()

        # 表名
        table_name = year + "-" + "pro"
        table_content = []
        print("表名:", table_name)
        # 表内容(原表)
        source_table_content = []
        for item in page_soup.find(class_="lqtable").find_all(name="td"):
            source_table_content.append(item.string)
        # 表头
        table_head = ["地区", "批次", "类别", "分数线"]
        print("表头:", table_head)
        source_table_content = source_table_content[5:]
        for i in range(0, len(source_table_content), 5):
            temp = []
            for j in range(5):
                if source_table_content[i + j] is None:
                    temp.append("-")
                    continue
                temp.append(source_table_content[i + j])
            table_content.append(temp)
        # 表项分项处理
        temp_table_content = []
        for item in table_content:
            # 跳过空项
            if item[2] == "-" and item[3] == "-" and item[4] == "-":
                continue
            # 特殊批次（其它分数线）
            if item[2] == "-" and item[3] == "-" and item[4] != "-":
                # 地区、批次、类别、分数线
                temp_item = [item[0], item[1], "其它", item[4]]
                temp_table_content.append(temp_item)
                continue
            # 文理分开
            if item[2] != "-":
                # 文科
                temp_item = [item[0], item[1], "文史", item[2]]
                temp_table_content.append(temp_item)
            if item[3] != "-":
                # 理科
                temp_item = [item[0], item[1], "理工", item[3]]
                temp_table_content.append(temp_item)
        # 设置批次
        for i in range(len(temp_table_content)):
            if temp_table_content[i][1] == "-":
                temp_table_content[i][1] = "一批"
        table_content = temp_table_content
        for item in table_content:
            print(item)
        # 将表内容写入文本文件
        file_path = "Information/九校联盟/北京大学/录取分数"
        write_table(file_path, table_name, table_head, table_content)


# 北京大学医学部录取分数
def get_score_info_pkuhsc():
    main_url = "http://jiaoyuchu.bjmu.edu.cn/zsjy/zsgz/lnfs"
    page_urls = ["194116", "187052", "183832", "176388"]
    file_path = "Information/九校联盟/北京大学医学部/录取分数"

    # 各年录取分数表
    # get_score_info_pkuhsc_table_2017(main_url, page_urls[0], file_path)
    # get_score_info_pkuhsc_table_2016(main_url, page_urls[1], file_path)
    # get_score_info_pkuhsc_table_2015(main_url, page_urls[2], file_path)
    # get_score_info_pkuhsc_table_2014(main_url, page_urls[3], file_path)


# 北大医学部2017年表
def get_score_info_pkuhsc_table_2017(main_url, url, file_path):
    # 表1
    specific_url = main_url + "/" + url
    page_source = requests.get(specific_url)
    page_source.encoding = "utf-8"
    page_soup = BeautifulSoup(page_source.text, "lxml")
    page_soup.prettify()
    # # 表名
    # table_name = page_soup.find(class_="bt1").text
    # print("表名", table_name)
    table_content = []
    for item in page_soup.find(name="table", attrs={"style": "width: 888px; border-collapse: collapse"}) \
            .find_all(name="tr"):
        temp = []
        for sub_item in item.find_all(name="td"):
            temp.append(sub_item.text.strip().replace('\n', ''))
            # print(sub_item.text)
        table_content.append(temp)
    # 表头
    table_head = table_content[0]
    table_head[0] = "地区"
    # print(table_head)
    table_content = table_content[1:]
    # 表项分项处理，每项为一个文件，year-district-major,提档线（分省）year-pro
    year = "2017"
    # 分省数据表
    sub_pro_table_name = year + "-" + "pro"
    sub_pro_table_head = ["地区", "批次", "类别", "分数线"]
    sub_pro_table_content = []
    for item in table_content:
        district_list = re.findall(r"(.*)[(]", item[0])
        district = item[0]
        if len(district_list) != 0:
            district = district_list[0]
        batch_list = re.findall(r"[(](.*)[)]", item[0])
        batch = "一批"
        if len(batch_list) != 0:
            batch = batch_list[0]
        temp = [district, batch, "医科", item[1]]
        sub_pro_table_content.append(temp)
    write_table(file_path, sub_pro_table_name, sub_pro_table_head, sub_pro_table_content)
    # print("表名：", sub_pro_table_name)
    # print("表头：", sub_pro_table_head)
    # for item in sub_pro_table_content:
    #     print(item)
    for item in table_content:
        sub_major_table_name = year + "-" + item[0] + "-" + "major"
        sub_major_table_head = ["专业", "类别", "最高分", "平均分", "最低分", "人数"]
        sub_major_table_content = []
        major_list = table_head
        for i in range(2, len(item)):
            if item[i] != "":
                temp = [major_list[i], "医科", "-", "-", item[i], "-"]
                sub_major_table_content.append(temp)
        write_table(file_path, sub_major_table_name, sub_major_table_head, sub_major_table_content)
        # print("表名：", sub_major_table_name)
        # print("表头：", sub_major_table_head)
        # for item in sub_major_table_content:
        #     print(item)


# 北大医学部2016年表
def get_score_info_pkuhsc_table_2016(main_url, url, file_path):
    # 表1
    specific_url = main_url + "/" + url
    page_source = requests.get(specific_url)
    page_source.encoding = "utf-8"
    page_soup = BeautifulSoup(page_source.text, "lxml")
    page_soup.prettify()
    # 表名
    # table_name = page_soup.find(class_="bt1").text
    # print("表名", table_name)
    table_content = []
    for item in page_soup.find(name="table", attrs={
        "style": "width: 1497px; border-collapse: collapse; margin: auto auto auto -0.25pt"}) \
            .find_all(name="tr"):
        temp = []
        for sub_item in item.find_all(name="td"):
            temp.append(sub_item.text.strip().replace('\n', ''))
            # print(sub_item.text)
        table_content.append(temp)
    # 表头
    table_head = table_content[0]
    table_head[0] = "地区"
    print("表头", table_head)
    table_content = table_content[2:]
    # 去除表尾备注
    table_content = table_content[:-3]
    # 表项分项处理，每项为一个文件，year-district-major,提档线（分省）year-pro
    year = "2016"
    # 分省数据表
    sub_pro_table_name = year + "-" + "pro"
    sub_pro_table_head = ["地区", "批次", "类别", "分数线"]
    sub_pro_table_content = []
    for item in table_content:
        district = item[0]
        batch = "一批"
        temp = [district, batch, "医科", item[1]]
        sub_pro_table_content.append(temp)
    # 去除新疆民族预科
    sub_pro_table_content.pop(len(sub_pro_table_content) - 1)
    write_table(file_path, sub_pro_table_name, sub_pro_table_head, sub_pro_table_content)
    print("表名：", sub_pro_table_name)
    print("表头：", sub_pro_table_head)
    for item in sub_pro_table_content:
        print(item)
    # 分专业数据表(去除新疆预科、港澳台联招另外添加)
    for item in table_content[:-1]:
        sub_major_table_name = year + "-" + item[0] + "-" + "major"
        sub_major_table_head = ["专业", "类别", "最高分", "平均分", "最低分", "人数"]
        sub_major_table_content = []
        major_list = table_head
        for i in range(2, len(item) - 2, 3):
            if item[i] != "" or item[i + 1] != "" or item[i + 2] != "":
                highest = item[i]
                lowest = item[i + 1]
                average = item[i + 2]
                if item[i] == "":
                    highest = "-"
                if item[i + 1] == "":
                    lowest = "-"
                if item[i + 2] == "":
                    average = "-"
                major = major_list[int((i - 2) / 3) + 2]
                temp = [major, "医科", highest, average, lowest, "-"]
                sub_major_table_content.append(temp)
        # 去除宁夏的最后一项（港澳台联招数据）
        if item[0] == "宁夏":
            sub_major_table_content.pop(len(sub_major_table_content) - 1)
        write_table(file_path, sub_major_table_name, sub_major_table_head, sub_major_table_content)
        print("表名：", sub_major_table_name)
        print("表头：", sub_major_table_head)
        for item in sub_major_table_content:
            print(item)
    # 添加新疆民族预科数据
    sub_major_table_name = year + "-" + "新疆民族预科" + "-" + "major"
    sub_major_table_head = ["专业", "类别", "最高分", "平均分", "最低分", "人数"]
    sub_major_table_content = [["药学（六年制）", "医科", "673", "652", "620", "-"],
                               ["医学实验技术（四年制）", "医科", "664", "630.5", "606", "-"]]
    write_table(file_path, sub_major_table_name, sub_major_table_head, sub_major_table_content)

    # 添加港澳台联招
    sub_major_table_name = year + "-" + "港澳台联招" + "-" + "major"
    sub_major_table_head = ["专业", "类别", "最高分", "平均分", "最低分", "人数"]
    sub_major_table_content = [["临床医学（六年制）", "医科", "634", "604.6", "577", "-"]]
    write_table(file_path, sub_major_table_name, sub_major_table_head, sub_major_table_content)

    # 国家专项附表
    table_content = []
    for item in page_soup.find(name="table", attrs={"style": "width: 898px; border-collapse: collapse"}) \
            .find_all(name="tr"):
        temp = []
        for sub_item in item.find_all(name="td"):
            temp.append(sub_item.text.strip().replace('\n', ''))
            # print(sub_item.text)
        table_content.append(temp)
    table_head = table_content[1]
    print(table_head)
    table_content = table_content[3:-1]
    for item in table_content:
        sub_major_table_name = year + "-" + item[0] + "国家专项" + "-" + "major"
        sub_major_table_head = ["专业", "类别", "最高分", "平均分", "最低分", "人数"]
        sub_major_table_content = []
        major_list = table_head
        for i in range(1, len(item) - 2, 3):
            if item[i] != "" or item[i + 1] != "" or item[i + 2] != "":
                highest = item[i]
                lowest = item[i + 1]
                average = item[i + 2]
                if item[i] == "":
                    highest = "-"
                if item[i + 1] == "":
                    lowest = "-"
                if item[i + 2] == "":
                    average = "-"
                major = major_list[int((i - 2) / 3) + 2]
                temp = [major, "医科", highest, average, lowest, "-"]
                sub_major_table_content.append(temp)
        write_table(file_path, sub_major_table_name, sub_major_table_head, sub_major_table_content)
        print("表名：", sub_major_table_name)
        print("表头：", sub_major_table_head)
        for item in sub_major_table_content:
            print(item)


# 北大医学部2015年表
def get_score_info_pkuhsc_table_2015(main_url, url, file_path):
    # 表1
    specific_url = main_url + "/" + url
    page_source = requests.get(specific_url)
    page_source.encoding = "utf-8"
    page_soup = BeautifulSoup(page_source.text, "lxml")
    page_soup.prettify()
    # 表名
    table_name = page_soup.find(class_="bt1").text
    print("表名", table_name)
    table_content = []
    for item in page_soup.find(name="table", attrs={
        "style": "border-top: medium none; border-right: medium none; "
                 "border-collapse: collapse; border-bottom: medium none; border-left: medium none"}) \
            .find_all(name="tr"):
        temp = []
        for sub_item in item.find_all(name="td"):
            temp.append(sub_item.text.strip().replace('\n', ''))
            # print(sub_item.text)
        table_content.append(temp)
    # 表头
    table_head = table_content[0]
    table_head[0] = "地区"
    print(table_head)
    table_content = table_content[2:]
    # 去除表尾备注
    table_content = table_content[:-15]
    # 表项分项处理，每项为一个文件，year-district-major,提档线（分省）year-pro
    year = "2015"
    # 分省数据表
    sub_pro_table_name = year + "-" + "pro"
    sub_pro_table_head = ["地区", "批次", "类别", "分数线"]
    sub_pro_table_content = []
    for item in table_content:
        district = item[0]
        batch = "一批"
        temp = [district, batch, "医科", item[1]]
        sub_pro_table_content.append(temp)
    write_table(file_path, sub_pro_table_name, sub_pro_table_head, sub_pro_table_content)
    print("表名：", sub_pro_table_name)
    print("表头：", sub_pro_table_head)
    for item in sub_pro_table_content:
        print(item)
    # 分专业数据表(去除港澳台联招另外添加)
    for item in table_content:
        sub_major_table_name = year + "-" + item[0] + "-" + "major"
        sub_major_table_head = ["专业", "类别", "最高分", "平均分", "最低分", "人数"]
        sub_major_table_content = []
        major_list = table_head
        for i in range(2, len(item) - 2, 3):
            if item[i] != "" or item[i + 1] != "" or item[i + 2] != "":
                highest = item[i]
                lowest = item[i + 1]
                average = item[i + 2]
                if item[i] == "":
                    highest = "-"
                if item[i + 1] == "":
                    lowest = "-"
                if item[i + 2] == "":
                    average = "-"
                major = major_list[int((i - 2) / 3) + 2]
                temp = [major, "医科", highest, average, lowest, "-"]
                sub_major_table_content.append(temp)
        # 去除宁夏、新疆的最后一项（港澳台联招数据）
        if item[0] == "宁夏" or item[0] == "新疆":
            sub_major_table_content.pop(len(sub_major_table_content) - 1)
        write_table(file_path, sub_major_table_name, sub_major_table_head, sub_major_table_content)
        print("表名：", sub_major_table_name)
        print("表头：", sub_major_table_head)
        for item in sub_major_table_content:
            print(item)

    # 添加港澳台联招
    sub_major_table_name = year + "-" + "港澳台联招" + "-" + "major"
    sub_major_table_head = ["专业", "类别", "最高分", "平均分", "最低分", "人数"]
    sub_major_table_content = [["临床医学（六年制）", "医科", "619", "613.4", "607", "-"]]
    write_table(file_path, sub_major_table_name, sub_major_table_head, sub_major_table_content)

    # 国家专项附表
    table_content = []
    for item in page_soup.find(name="table", attrs={
        "style": "width: 907px; border-collapse: collapse; margin: auto auto auto -0.25pt"}) \
            .find_all(name="tr"):
        temp = []
        for sub_item in item.find_all(name="td"):
            temp.append(sub_item.text.strip().replace('\n', ''))
            # print(sub_item.text)
        table_content.append(temp)
    table_name = "2015" + table_content[0][0]
    table_head = table_content[1]
    print(table_name)
    print(table_head)
    table_content = table_content[3:-1]
    # 分省数据表
    sub_pro_table_name = year + "-" + "国家专项" + "-" + "pro"
    sub_pro_table_head = ["地区", "批次", "类别", "分数线"]
    sub_pro_table_content = []
    for item in table_content:
        district = item[0]
        batch = "国家专项"
        temp = [district, batch, "医科", item[1]]
        sub_pro_table_content.append(temp)
    write_table(file_path, sub_pro_table_name, sub_pro_table_head, sub_pro_table_content)
    print("表名：", sub_pro_table_name)
    print("表头：", sub_pro_table_head)
    for item in sub_pro_table_content:
        print(item)
    # 分专业数据表
    for item in table_content:
        sub_major_table_name = year + "-" + item[0] + "国家专项" + "-" + "major"
        sub_major_table_head = ["专业", "类别", "最高分", "平均分", "最低分", "人数"]
        sub_major_table_content = []
        major_list = table_head
        for i in range(2, len(item) - 2, 3):
            if item[i] != "" or item[i + 1] != "" or item[i + 2] != "":
                highest = item[i]
                lowest = item[i + 1]
                average = item[i + 2]
                if item[i] == "":
                    highest = "-"
                if item[i + 1] == "":
                    lowest = "-"
                if item[i + 2] == "":
                    average = "-"
                major = major_list[int((i - 2) / 3) + 2]
                temp = [major, "医科", highest, average, lowest, "-"]
                sub_major_table_content.append(temp)
        write_table(file_path, sub_major_table_name, sub_major_table_head, sub_major_table_content)
        print("表名：", sub_major_table_name)
        print("表头：", sub_major_table_head)
        for item in sub_major_table_content:
            print(item)


# 北大医学部2014年表
def get_score_info_pkuhsc_table_2014(main_url, url, file_path):
    # 表1
    specific_url = main_url + "/" + url
    page_source = requests.get(specific_url)
    page_source.encoding = "utf-8"
    page_soup = BeautifulSoup(page_source.text, "lxml")
    page_soup.prettify()
    # 表名
    # table_name = page_soup.find(class_="bt1").text
    # print("表名", table_name)
    table_content = []
    for item in list(page_soup.find(text="2014年北京大学医学部本科生各专业录取分数").parents)[5].find_all(name="tr"):
        temp = []
        for sub_item in item.find_all(name="td"):
            temp.append(sub_item.text.strip().replace('\n', ''))
            # print(sub_item.text)
        table_content.append(temp)
    # 表头
    table_head = []
    table_content[1].pop(0)
    for i in range(len(table_content[1])):
        table_head.append(table_content[1][i] + table_content[2][i])
    table_head.insert(0, "地区")
    print(table_head)
    table_content = table_content[4:]
    # 去除表尾备注
    table_content = table_content[:-1]
    # 表项分项处理，每项为一个文件，year-district-major,提档线（分省）year-pro
    year = "2014"
    # 分专业数据表(去除港澳台联招另外添加)
    for item in table_content:
        sub_major_table_name = year + "-" + item[0] + "-" + "major"
        sub_major_table_head = ["专业", "类别", "最高分", "平均分", "最低分", "人数"]
        sub_major_table_content = []
        major_list = table_head
        for i in range(1, len(item) - 2, 3):
            if item[i] != "" or item[i + 1] != "" or item[i + 2] != "":
                highest = item[i]
                lowest = item[i + 1]
                average = item[i + 2]
                if item[i] == "":
                    highest = "-"
                if item[i + 1] == "":
                    lowest = "-"
                if item[i + 2] == "":
                    average = "-"
                major = major_list[int((i - 2) / 3) + 2]
                temp = [major, "医科", highest, average, lowest, "-"]
                sub_major_table_content.append(temp)
        write_table(file_path, sub_major_table_name, sub_major_table_head, sub_major_table_content)
        print("表名：", sub_major_table_name)
        print("表头：", sub_major_table_head)
        for item in sub_major_table_content:
            print(item)
    # 添加港澳台联招
    sub_major_table_name = year + "-" + "港澳台联招" + "-" + "major"
    sub_major_table_head = ["专业", "类别", "最高分", "平均分", "最低分", "人数"]
    sub_major_table_content = [["临床医学（六年制）", "医科", "680", "636", "576", "-"]]
    write_table(file_path, sub_major_table_name, sub_major_table_head, sub_major_table_content)

    # 一批本科提档线
    table_content_pro = []
    for item in list(page_soup.find(text="医学部2014年各省一批本科提档线").parents)[5].find_all(name="tr")[2:]:
        for sub_item in item.find_all(name="td"):
            table_content_pro.append(sub_item.text.strip().replace('\n', ''))
    # 分省数据表
    sub_pro_table_name = year + "-" + "pro"
    sub_pro_table_head = ["地区", "批次", "类别", "分数线"]
    sub_pro_table_content = []
    for i in range(0, len(table_content_pro), 2):
        district = table_content_pro[i]
        line = table_content_pro[i + 1]
        batch = "一批"
        temp = [district, batch, "医科", line]
        sub_pro_table_content.append(temp)

    write_table(file_path, sub_pro_table_name, sub_pro_table_head, sub_pro_table_content)
    print("表名：", sub_pro_table_name)
    print("表头：", sub_pro_table_head)
    for item in sub_pro_table_content:
        print(item)


# 清华大学录取分数
def get_score_info_tsinghua():
    # main_url = "http://www.join-tsinghua.edu.cn"
    # url = main_url + "/publish/bzw/7541/index.html"
    # page_source = requests.get(url)
    # page_source.encoding = page_source.apparent_encoding
    # page_soup = BeautifulSoup(page_source.text, "lxml")
    # page_soup.prettify()
    main_file_path = "Information/九校联盟/清华大学/录取分数"
    # 下载文件
    # print("开始下载文件")
    # for item in page_soup.find("ul", class_="ulList").find_all("li"):
    #     specific_url = main_url + item.a["href"]
    #     sub_page_source = requests.get(specific_url)
    #     sub_page_source.encoding = sub_page_source.apparent_encoding
    #     sub_page_soup = BeautifulSoup(sub_page_source.text, "lxml")
    #     sub_page_soup.prettify()
    #     file_name = sub_page_soup.find("a", text=re.compile("附件|xls|pdf")).text
    #     file_url = sub_page_soup.find("a", text=re.compile("附件|xls|pdf"))["href"]
    #     file_name = file_name[:file_name.find(".")] + file_url[file_url.find("."):]
    #     file_content = requests.get(main_url + file_url)
    #     with open(main_file_path + "/source/" + file_name, "wb") as pdf:
    #         pdf.write(file_content.content)
    # print("文件下载完成！")

    # 文件解析
    print("开始文件解析")
    file_list = read_all_file_list(main_file_path + "/source")
    file_major = []
    file_pro = []
    for file in file_list:
        if file.find("最低") != -1:
            file_pro.append(file)
        else:
            file_major.append(file)
    # for item in file_major:
    #     print(item)
    # print("-------------")
    # for item in file_pro:
    #     print(item)

    # 分省录取分数线数据解析
    # for item in file_pro:
    #     year_se = re.search("\d{4}", item).span()
    #     start_year = item[year_se[0]:year_se[1]]
    #     sub_pro_table_name = start_year + "-" + "pro"
    #     sub_pro_table_head = ["地区", "批次", "类别", "分数线"]
    #     if start_year == "2006":
    #         table2006 = get_score_pro_info_tsinghua_2006_2008(item)
    #         write_table(main_file_path, sub_pro_table_name, sub_pro_table_head, table2006[0])
    #     if start_year == "2007":
    #         table2007 = get_score_pro_info_tsinghua_2007_2009(item)
    #         write_table(main_file_path, sub_pro_table_name, sub_pro_table_head, table2007[0])
    #     if start_year == "2008":
    #         table2008 = get_score_pro_info_tsinghua_2008_2010(item)
    #         write_table(main_file_path, sub_pro_table_name, sub_pro_table_head, table2008[0])
    #     if start_year == "2009":
    #         table2009 = get_score_pro_info_tsinghua_2009_2011(item)
    #         write_table(main_file_path, sub_pro_table_name, sub_pro_table_head, table2009[0])
    #     if start_year == "2010":
    #         table2010 = get_score_pro_info_tsinghua_2010_2012(item)
    #         write_table(main_file_path, sub_pro_table_name, sub_pro_table_head, table2010[0])
    #     if start_year == "2011":
    #         table2011 = get_score_pro_info_tsinghua_2011_2013(item)
    #         write_table(main_file_path, sub_pro_table_name, sub_pro_table_head, table2011[0])
    #         write_table(main_file_path, "2012-pro", sub_pro_table_head, table2011[1])
    #         write_table(main_file_path, "2013-pro", sub_pro_table_head, table2011[2])

    # 分专业录取分数数据解析
    for item in file_major:
        year_se = re.search("\d{4}", item).span()
        start_year = item[year_se[0]:year_se[1]]
        # if start_year == "2006":
        #     write_score_major_info_tsinghua_2006_2008(main_file_path, item)
        # if start_year == "2007":
        #     write_score_major_info_tsinghua_2007_2009(main_file_path, item)
        # if start_year == "2008":
        #     write_score_major_info_tsinghua_2008_2010(main_file_path, item)
        # if start_year == "2009":
        #     write_score_major_info_tsinghua_2009_2011(main_file_path, item)
        # if start_year == "2010":
        #     write_score_major_info_tsinghua_2010_2012(main_file_path, item)
        if start_year == "2011":
            write_score_major_info_tsinghua_2011_2013(main_file_path, item)


def get_score_pro_info_tsinghua_2006_2008(info_path):
    year_list = ["2006", "2007", "2008"]
    excel_file = read_xls(info_path)
    sheet = excel_file.sheet_by_index(0)
    source_table = []
    for i_row in range(sheet.nrows):
        source_table.append(sheet.row_values(i_row)[1:])
    source_table = source_table[5:-1]
    return_table = []
    for i_year in range(len(year_list)):
        sub_pro_table_name = year_list[i_year] + "-" + "pro"
        sub_pro_table_head = ["地区", "批次", "类别", "分数线"]
        sub_pro_table_content = []
        for item in source_table:
            if item[i_year * 4 + 1] != "":
                temp = [item[0], "一批", "理工", str(item[i_year * 4 + 1]).replace(".0", "")]
                sub_pro_table_content.append(temp)
            if item[i_year * 4 + 2] != "":
                temp = [item[0], "", "国防定向", str(item[i_year * 4 + 2]).replace(".0", "")]
                sub_pro_table_content.append(temp)
            if item[i_year * 4 + 3] != "":
                temp = [item[0], "", "其他定向", str(item[i_year * 4 + 3]).replace(".0", "")]
                sub_pro_table_content.append(temp)
            if item[i_year * 4 + 4] != "":
                temp = [item[0], "一批", "文史", str(item[i_year * 4 + 4]).replace(".0", "")]
                sub_pro_table_content.append(temp)
        return_table.append(sub_pro_table_content)
        # print(sub_pro_table_name)
        # for item in sub_pro_table_content:
        #     print(item)
    return return_table


def get_score_pro_info_tsinghua_2007_2009(info_path):
    year_list = ["2007", "2008", "2009"]
    excel_file = read_xls(info_path)
    sheet = excel_file.sheet_by_index(0)
    source_table = []
    for i_row in range(sheet.nrows):
        source_table.append(sheet.row_values(i_row))
    source_table = source_table[3:-1]
    return_table = []
    for i_year in range(len(year_list)):
        sub_pro_table_name = year_list[i_year] + "-" + "pro"
        sub_pro_table_head = ["地区", "批次", "类别", "分数线"]
        sub_pro_table_content = []
        for item in source_table:
            if item[i_year * 4 + 1] != "":
                temp = [item[0], "一批", "理工", str(item[i_year * 4 + 1]).replace(".0", "")]
                sub_pro_table_content.append(temp)
            if item[i_year * 4 + 2] != "":
                temp = [item[0], "", "国防定向", str(item[i_year * 4 + 2]).replace(".0", "")]
                sub_pro_table_content.append(temp)
            if item[i_year * 4 + 3] != "":
                temp = [item[0], "", "其他定向", str(item[i_year * 4 + 3]).replace(".0", "")]
                sub_pro_table_content.append(temp)
            if item[i_year * 4 + 4] != "":
                temp = [item[0], "一批", "文史", str(item[i_year * 4 + 4]).replace(".0", "")]
                sub_pro_table_content.append(temp)
        return_table.append(sub_pro_table_content)
        # print(sub_pro_table_name)
        # for item in sub_pro_table_content:
        #     print(item)
    return return_table


def get_score_pro_info_tsinghua_2008_2010(info_path):
    year_list = ["2008", "2009", "2010"]
    excel_file = read_xls(info_path)
    sheet = excel_file.sheet_by_index(0)
    source_table = []
    for i_row in range(sheet.nrows):
        source_table.append(sheet.row_values(i_row))
    source_table = source_table[3:-1]
    return_table = []
    for i_year in range(len(year_list)):
        sub_pro_table_name = year_list[i_year] + "-" + "pro"
        sub_pro_table_head = ["地区", "批次", "类别", "分数线"]
        sub_pro_table_content = []
        for item in source_table:
            if item[i_year * 4 + 1] != "":
                temp = [item[0], "一批", "理工", str(item[i_year * 4 + 1]).replace(".0", "")]
                sub_pro_table_content.append(temp)
            if item[i_year * 4 + 2] != "":
                temp = [item[0], "", "国防定向", str(item[i_year * 4 + 2]).replace(".0", "")]
                sub_pro_table_content.append(temp)
            if item[i_year * 4 + 3] != "":
                temp = [item[0], "", "其他定向", str(item[i_year * 4 + 3]).replace(".0", "")]
                sub_pro_table_content.append(temp)
            if item[i_year * 4 + 4] != "":
                temp = [item[0], "一批", "文史", str(item[i_year * 4 + 4]).replace(".0", "")]
                sub_pro_table_content.append(temp)
        return_table.append(sub_pro_table_content)
        # print(sub_pro_table_name)
        # for item in sub_pro_table_content:
        #     print(item)
    return return_table


def get_score_pro_info_tsinghua_2009_2011(info_path):
    year_list = ["2009", "2010", "2011"]
    excel_file = read_xls(info_path)
    sheet = excel_file.sheet_by_index(0)
    source_table = []
    for i_row in range(sheet.nrows):
        source_table.append(sheet.row_values(i_row))
    source_table = source_table[3:-1]
    # for item in source_table:
    #     print(item)
    return_table = []
    for i_year in range(len(year_list)):
        sub_pro_table_name = year_list[i_year] + "-" + "pro"
        sub_pro_table_head = ["地区", "批次", "类别", "分数线"]
        sub_pro_table_content = []
        for item in source_table:
            if item[i_year * 4 + 1] != "":
                temp = [item[0], "一批", "理工", str(item[i_year * 4 + 1]).replace(".0", "")]
                sub_pro_table_content.append(temp)
            if item[i_year * 4 + 2] != "":
                temp = [item[0], "", "国防定向", str(item[i_year * 4 + 2]).replace(".0", "")]
                sub_pro_table_content.append(temp)
            if item[i_year * 4 + 3] != "":
                temp = [item[0], "", "其他定向", str(item[i_year * 4 + 3]).replace(".0", "")]
                sub_pro_table_content.append(temp)
            if item[i_year * 4 + 4] != "":
                temp = [item[0], "一批", "文史", str(item[i_year * 4 + 4]).replace(".0", "")]
                sub_pro_table_content.append(temp)
        return_table.append(sub_pro_table_content)
        # print(sub_pro_table_name)
        # for item in sub_pro_table_content:
        #     print(item)
    return return_table


def get_score_pro_info_tsinghua_2010_2012(info_path):
    year_list = ["2010", "2011", "2012"]
    excel_file = read_xls(info_path)
    sheet = excel_file.sheet_by_index(0)
    source_table = []
    for i_row in range(sheet.nrows):
        source_table.append(sheet.row_values(i_row))
    source_table = source_table[3:-1]
    # for item in source_table:
    #     print(item)
    return_table = []
    for i_year in range(len(year_list)):
        sub_pro_table_name = year_list[i_year] + "-" + "pro"
        sub_pro_table_head = ["地区", "批次", "类别", "分数线"]
        sub_pro_table_content = []
        for item in source_table:
            if item[i_year * 4 + 1] != "":
                temp = [item[0], "一批", "理工", str(item[i_year * 4 + 1]).replace(".0", "")]
                sub_pro_table_content.append(temp)
            if item[i_year * 4 + 2] != "":
                temp = [item[0], "", "国防定向", str(item[i_year * 4 + 2]).replace(".0", "")]
                sub_pro_table_content.append(temp)
            if item[i_year * 4 + 3] != "":
                temp = [item[0], "", "其他定向", str(item[i_year * 4 + 3]).replace(".0", "")]
                sub_pro_table_content.append(temp)
            if item[i_year * 4 + 4] != "":
                temp = [item[0], "一批", "文史", str(item[i_year * 4 + 4]).replace(".0", "")]
                sub_pro_table_content.append(temp)
        return_table.append(sub_pro_table_content)
        # print(sub_pro_table_name)
        # for item in sub_pro_table_content:
        #     print(item)
    return return_table


def get_score_pro_info_tsinghua_2011_2013(info_path):
    year_list = ["2011", "2012", "2013"]
    excel_file = read_xls(info_path)
    sheet = excel_file.sheet_by_index(0)
    source_table = []
    for i_row in range(sheet.nrows):
        source_table.append(sheet.row_values(i_row))
    source_table = source_table[3:-1]
    # for item in source_table:
    #     print(item)
    return_table = []
    for i_year in range(len(year_list)):
        sub_pro_table_name = year_list[i_year] + "-" + "pro"
        sub_pro_table_head = ["地区", "批次", "类别", "分数线"]
        sub_pro_table_content = []
        for item in source_table:
            if item[i_year * 4 + 1] != "":
                temp = [item[0], "一批", "理工", str(item[i_year * 4 + 1]).replace(".0", "")]
                sub_pro_table_content.append(temp)
            if item[i_year * 4 + 2] != "":
                temp = [item[0], "", "国防定向", str(item[i_year * 4 + 2]).replace(".0", "")]
                sub_pro_table_content.append(temp)
            if item[i_year * 4 + 3] != "":
                temp = [item[0], "", "其他定向", str(item[i_year * 4 + 3]).replace(".0", "")]
                sub_pro_table_content.append(temp)
            if item[i_year * 4 + 4] != "":
                temp = [item[0], "一批", "文史", str(item[i_year * 4 + 4]).replace(".0", "")]
                sub_pro_table_content.append(temp)
        return_table.append(sub_pro_table_content)
        # print(sub_pro_table_name)
        # for item in sub_pro_table_content:
        #     print(item)
    return return_table


def write_score_major_info_tsinghua_2006_2008(store_path, info_path):
    year_list = ["2006", "2007", "2008"]
    excel_file = read_xls(info_path)
    sheet_names = excel_file.sheet_names()
    for i_year in range(len(year_list)):
        for sheet_name in sheet_names:
            sheet = excel_file.sheet_by_name(sheet_name)
            pro_list = sheet_name.split("、")
            source_table = []
            for i_row in range(sheet.nrows):
                source_table.append(sheet.row_values(i_row)[:-1])
            if sheet_name == sheet_names[0]:
                source_table = source_table[4:-2]
            else:
                source_table = source_table[3:-2]
            for i_pro in range(len(pro_list)):
                if pro_list[i_pro] == "内蒙":
                    name_pro = "内蒙古"
                else:
                    name_pro = pro_list[i_pro]
                sub_pro_table_name = year_list[i_year] + "-" + name_pro + "-" + "major"
                sub_pro_table_head = ["专业", "类别", "最高分", "平均分", "最低分", "人数"]
                sub_pro_table_content = []
                for item in source_table:
                    if item[i_pro * 9 + i_year * 3 + 1] != "" and item[i_pro * 9 + i_year * 3 + 1] != 0:
                        classy_search_list = re.findall(r"[（](.*)[）]", item[0])
                        if len(classy_search_list) == 0:
                            classy = "理工"
                        else:
                            classy = classy_search_list[0]
                        if classy == "文":
                            classy = "文史"
                        if item[0] == "临床医学":
                            classy = "医科"
                        temp = [item[0], classy, str(item[i_pro * 9 + i_year * 3 + 2]).replace(".0", ""),
                                str(item[i_pro * 9 + i_year * 3 + 1]),
                                str(item[i_pro * 9 + i_year * 3 + 3]).replace(".0", ""), "-"]
                        sub_pro_table_content.append(temp)
                # 此表只写入2006年的数据
                if i_year == 0:
                    write_table(store_path, sub_pro_table_name, sub_pro_table_head, sub_pro_table_content)
                print(sub_pro_table_name)
                for item in sub_pro_table_content:
                    print(item)
                print("-------------------")


def write_score_major_info_tsinghua_2007_2009(store_path, info_path):
    year_list = ["2007", "2008", "2009"]
    excel_file = read_xls(info_path)
    sheet_names = excel_file.sheet_names()
    for i_year in range(len(year_list)):
        for sheet_name in sheet_names:
            sheet = excel_file.sheet_by_name(sheet_name)
            pro_list = sheet_name.split(" ")
            source_table = []
            for i_row in range(sheet.nrows):
                source_table.append(sheet.row_values(i_row)[:-1])
            source_table = source_table[4:-2]
            for i_pro in range(len(pro_list)):
                if pro_list[i_pro] == "内蒙":
                    name_pro = "内蒙古"
                else:
                    name_pro = pro_list[i_pro]
                sub_pro_table_name = year_list[i_year] + "-" + name_pro + "-" + "major"
                sub_pro_table_head = ["专业", "类别", "最高分", "平均分", "最低分", "人数"]
                sub_pro_table_content = []
                for item in source_table:
                    if item[i_pro * 9 + i_year * 3 + 1] != "" and item[i_pro * 9 + i_year * 3 + 1] != 0:
                        classy_search_list = re.findall(r"[（](.*)[）]", item[0])
                        if len(classy_search_list) == 0:
                            classy = "理工"
                        else:
                            classy = classy_search_list[0]
                        if classy == "文":
                            classy = "文史"
                        if classy == "理":
                            classy = "理工"
                        if item[0] == "临床医学":
                            classy = "医科"
                        temp = [item[0], classy, str(item[i_pro * 9 + i_year * 3 + 2]).replace(".0", ""),
                                str(item[i_pro * 9 + i_year * 3 + 1]),
                                str(item[i_pro * 9 + i_year * 3 + 3]).replace(".0", ""), "-"]
                        sub_pro_table_content.append(temp)
                # 此表只写入2007年的数据
                if i_year == 0:
                    write_table(store_path, sub_pro_table_name, sub_pro_table_head, sub_pro_table_content)
                print(sub_pro_table_name)
                for item in sub_pro_table_content:
                    print(item)
                print("-------------------")


def write_score_major_info_tsinghua_2008_2010(store_path, info_path):
    year_list = ["2008", "2009", "2010"]
    print("开始读取")
    pages = read_pdf_to_tables(info_path)
    for i_year in range(len(year_list)):
        for table in pages:
            temp_pro_list = table[0][0]
            pro_list = []
            for item in temp_pro_list:
                if item is not None and item != "专业":
                    pro_list.append(item)
            print(pro_list)
            source_table = []
            for line in table[0][3:-1]:
                source_table.append(line[:-1])
            for i_pro in range(len(pro_list)):
                if pro_list[i_pro] == "内蒙":
                    name_pro = "内蒙古"
                else:
                    name_pro = pro_list[i_pro]
                sub_pro_table_name = year_list[i_year] + "-" + name_pro + "-" + "major"
                sub_pro_table_head = ["专业", "类别", "最高分", "平均分", "最低分", "人数"]
                sub_pro_table_content = []
                for item in source_table:
                    if item[i_pro * 9 + i_year * 3 + 1] != "" and item[i_pro * 9 + i_year * 3 + 1] != 0:
                        classy_search_list = re.findall(r"[（](.*)[）]", item[0])
                        if len(classy_search_list) == 0:
                            classy = "理工"
                        else:
                            classy = classy_search_list[0]
                        if classy == "文":
                            classy = "文史"
                        if classy == "理":
                            classy = "理工"
                        if item[0] == "临床医学":
                            classy = "医科"
                        temp = [item[0], classy, str(item[i_pro * 9 + i_year * 3 + 2]).replace(".0", ""),
                                str(item[i_pro * 9 + i_year * 3 + 1]),
                                str(item[i_pro * 9 + i_year * 3 + 3]).replace(".0", ""), "-"]
                        sub_pro_table_content.append(temp)
                # 此表只写入2008年的数据
                if i_year == 0:
                    write_table(store_path, sub_pro_table_name, sub_pro_table_head, sub_pro_table_content)
                print(sub_pro_table_name)
                for item in sub_pro_table_content:
                    print(item)
                print("-------------------")


def write_score_major_info_tsinghua_2009_2011(store_path, info_path):
    year_list = ["2009", "2010", "2011"]
    excel_file = read_xls(info_path)
    sheet = excel_file.sheet_by_index(0)
    source_table = []
    for i_row in range(sheet.nrows):
        source_table.append(sheet.row_values(i_row))
    temp_pro_list = source_table[0]
    pro_list = []
    for item in temp_pro_list:
        if item != "" and item != "专业":
            pro_list.append(item)
    print(pro_list)
    source_table = source_table[3:]
    for item in source_table:
        print(item)
    for i_year in range(len(year_list)):
        for i_pro in range(len(pro_list)):
            if pro_list[i_pro] == "内蒙":
                name_pro = "内蒙古"
            else:
                name_pro = pro_list[i_pro]
            sub_pro_table_name = year_list[i_year] + "-" + name_pro + "-" + "major"
            sub_pro_table_head = ["专业", "类别", "最高分", "平均分", "最低分", "人数"]
            sub_pro_table_content = []
            for item in source_table:
                if item[i_pro * 9 + i_year * 3 + 1] != "" and item[i_pro * 9 + i_year * 3 + 1] != 0:
                    classy_search_list = re.findall(r"[（](.*)[）]", item[0])
                    if len(classy_search_list) == 0:
                        classy = "理工"
                    else:
                        classy = classy_search_list[0]
                    if classy == "文":
                        classy = "文史"
                    if classy == "理":
                        classy = "理工"
                    if item[0] == "临床医学":
                        classy = "医科"
                    temp = [item[0], classy, str(item[i_pro * 9 + i_year * 3 + 1]).replace(".0", ""),
                            str(item[i_pro * 9 + i_year * 3 + 3]),
                            str(item[i_pro * 9 + i_year * 3 + 2]).replace(".0", ""), "-"]
                    sub_pro_table_content.append(temp)
            # 此表只写入2009年的数据
            if i_year == 0:
                write_table(store_path, sub_pro_table_name, sub_pro_table_head, sub_pro_table_content)
            print(sub_pro_table_name)
            for item in sub_pro_table_content:
                print(item)
            print("-------------------")


def write_score_major_info_tsinghua_2010_2012(store_path, info_path):
    year_list = ["2010", "2011", "2012"]
    excel_file = read_xls(info_path)
    sheet = excel_file.sheet_by_index(0)
    source_table = []
    for i_row in range(sheet.nrows):
        source_table.append(sheet.row_values(i_row))
    temp_pro_list = source_table[0]
    pro_list = []
    for item in temp_pro_list:
        if item != "" and item != "专业":
            pro_list.append(item)
    print(pro_list)
    source_table = source_table[3:]
    for item in source_table:
        print(item)
    for i_year in range(len(year_list)):
        for i_pro in range(len(pro_list)):
            if pro_list[i_pro] == "内蒙":
                name_pro = "内蒙古"
            else:
                name_pro = pro_list[i_pro]
            sub_pro_table_name = year_list[i_year] + "-" + name_pro + "-" + "major"
            sub_pro_table_head = ["专业", "类别", "最高分", "平均分", "最低分", "人数"]
            sub_pro_table_content = []
            for item in source_table:
                if item[i_pro * 9 + i_year * 3 + 1] != "" and item[i_pro * 9 + i_year * 3 + 1] != 0:
                    classy_search_list = re.findall(r"[（](.*)[）]", item[0])
                    if len(classy_search_list) == 0:
                        classy = "理工"
                    else:
                        classy = classy_search_list[0]
                    if classy == "文":
                        classy = "文史"
                    if classy == "理":
                        classy = "理工"
                    if item[0] == "临床医学":
                        classy = "医科"
                    temp = [item[0], classy, str(item[i_pro * 9 + i_year * 3 + 1]).replace(".0", ""),
                            str(item[i_pro * 9 + i_year * 3 + 3]),
                            str(item[i_pro * 9 + i_year * 3 + 2]).replace(".0", ""), "-"]
                    sub_pro_table_content.append(temp)
            # 此表只写入2009年的数据
            if i_year == 0:
                write_table(store_path, sub_pro_table_name, sub_pro_table_head, sub_pro_table_content)
            print(sub_pro_table_name)
            for item in sub_pro_table_content:
                print(item)
            print("-------------------")


def write_score_major_info_tsinghua_2011_2013(store_path, info_path):
    year_list = ["2011", "2012", "2013"]
    excel_file = read_xls(info_path)
    sheet = excel_file.sheet_by_index(0)
    source_table = []
    for i_row in range(sheet.nrows):
        source_table.append(sheet.row_values(i_row))
    temp_pro_list = source_table[0]
    pro_list = []
    for item in temp_pro_list:
        if item != "" and item != "专业":
            pro_list.append(item)
    print(pro_list)
    source_table = source_table[3:]
    for item in source_table:
        print(item)
    for i_year in range(len(year_list)):
        for i_pro in range(len(pro_list)):
            if pro_list[i_pro] == "内蒙":
                name_pro = "内蒙古"
            else:
                name_pro = pro_list[i_pro]
            sub_pro_table_name = year_list[i_year] + "-" + name_pro + "-" + "major"
            sub_pro_table_head = ["专业", "类别", "最高分", "平均分", "最低分", "人数"]
            sub_pro_table_content = []
            for item in source_table:
                if item[i_pro * 9 + i_year * 3 + 1] != "" and item[i_pro * 9 + i_year * 3 + 1] != 0:
                    classy_search_list = re.findall(r"[（](.*)[）]", item[0])
                    if len(classy_search_list) == 0:
                        classy = "理工"
                    else:
                        classy = classy_search_list[0]
                    if classy == "文":
                        classy = "文史"
                    if classy == "理":
                        classy = "理工"
                    if item[0] == "临床医学":
                        classy = "医科"
                    temp = [item[0], classy, str(item[i_pro * 9 + i_year * 3 + 1]).replace(".0", ""),
                            str(item[i_pro * 9 + i_year * 3 + 3]),
                            str(item[i_pro * 9 + i_year * 3 + 2]).replace(".0", ""), "-"]
                    sub_pro_table_content.append(temp)
            write_table(store_path, sub_pro_table_name, sub_pro_table_head, sub_pro_table_content)
            print(sub_pro_table_name)
            for item in sub_pro_table_content:
                print(item)
            print("-------------------")


if __name__ == "__main__":
    print("begin...")
    get_score_info_hit()
    # get_score_info_pku()
    # get_score_info_pkuhsc()
    # get_score_info_tsinghua()
    print("end...")
