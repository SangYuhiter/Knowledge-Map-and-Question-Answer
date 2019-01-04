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
    main_url = "http://zsb.hit.edu.cn/information/plan"
    # 获取分类信息
    main_page_source = requests.get(main_url).text
    main_page_soup = BeautifulSoup(main_page_source, "lxml")
    main_page_soup.prettify()
    # 招生计划省份
    province = []
    for item in main_page_soup.find(class_="province").find_all(name='a'):
        province.append(item.string.strip())
    print("招生地区：", province)
    # 招生计划年份
    years = []
    for item in main_page_soup.find_all(class_="year-select"):
        years.append(item.string.strip())
    print("招生年份：", years)

    # 对每年份各省数据进行抽取
    for pro in province:
        for year in years:
            print("获取", year, pro, "的招生计划")
            # 构造链接
            specific_url = main_url + "?" + "year=" + year + "&" + "province=" + pro
            page_source = requests.get(specific_url).text
            page_soup = BeautifulSoup(page_source, "lxml")
            page_soup.prettify()
            # 表名
            table_name = year+"-"+pro
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
                if item[0] == "无数据":
                    table_content.remove(item)
                elif item[1] == "统计":
                    table_content.remove(item)
            for item in table_content:
                print(item)
            # 将表内容写入文本文件
            file_path = "Information/九校联盟/哈尔滨工业大学/招生计划"
            write_table(file_path, table_name, table_head, table_content)
            print(year, pro, "的招生计划已存入文件")


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
        table_head[1]="类别"
        table_content = table_content[1:]
        for i in range(len(table_content)):
            table_content[i][0]+=table_content[i][1]+"年"
            table_content[i][1]="医科"
        print(table_name)
        print(table_head)
        for item in table_content:
            print(item)
        file_path = "Information/九校联盟/北京大学/招生计划/医学部"
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
        file_path = "Information/九校联盟/北京大学/招生计划/医学部"
        write_table(file_path, table_name, table_head, table_content)


if __name__ == "__main__":
    print("start...")
    get_plan_info_hit()
    # get_plan_info_pku()
    # get_plan_info_pkuhsc()
    print("end...")
