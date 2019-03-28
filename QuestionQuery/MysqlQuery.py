# -*- coding: utf-8 -*-
"""
@File  : MysqlQuery.py
@Author: SangYu
@Date  : 2019/3/1 10:53
@Desc  : 处理MySQL表相关问题的查询
"""

from InformationGet.MysqlOperation import mysql_query_sentence


# mysql表查询，返回查询结果
def mysql_table_query(keyword):
    search_table = keyword["search_table"]
    if search_table == "admission_plan":
        query_result = admission_plan_table_query(keyword)
    elif search_table == "admission_score_pro":
        query_result = admission_score_pro_table_query(keyword)
    elif search_table == "admission_score_major":
        query_result = admission_score_major_table_query(keyword)
    return query_result


# 查询admission_plan表
def admission_plan_table_query(keyword):
    search_table = keyword["search_table"]
    search_year = keyword["search_year"]
    search_school = keyword["search_school"]
    search_major = keyword["search_major"]
    search_district = keyword["search_district"]
    result_edit = []
    # 只有年份,统计各学校的招生情况（文科、理科）
    if search_year != "" and search_school == "" and search_major == "" and search_district == "":
        # 查询学校该年招生总人数
        sql_string = "SELECT school,COUNT(*) FROM admission_plan WHERE year = '" + search_year \
                     + "' GROUP BY school;"
        myresult = mysql_query_sentence(sql_string)
        if len(myresult) == 0:
            result_edit.append("查询结果为空！")
        else:
            for item in myresult:
                result_edit.append(str(item[0]) + search_year + "年" + "招生计划为" + str(item[1]) + "人")
                # 查询该年该校招生的类别情况
                sub_sql_string = "SELECT classy,COUNT(*) FROM admission_plan WHERE year = '" + search_year \
                                 + "' and school = '" + str(item[0]) + "' GROUP BY classy;"
                # print(sub_sql_string)
                sub_myresult = mysql_query_sentence(sub_sql_string)
                if len(sub_myresult) == 0:
                    result_edit.append("招生类别查询结果为空！")
                else:
                    for item in sub_myresult:
                        result_edit.append("其中" + str(item[0]) + str(item[1]) + "人")
    # 只有学校，统计该学校的招生情况（文科理科）
    elif search_year == "" and search_school != "" and search_major == "" and search_district == "":
        # 查询学校各年招生总人数
        sql_string = "SELECT year,COUNT(*) FROM admission_plan WHERE school = '" + search_school \
                     + "' GROUP BY year;"
        myresult = mysql_query_sentence(sql_string)
        if len(myresult) == 0:
            result_edit.append("查询结果为空！")
        else:
            for item in myresult:
                result_edit.append(search_school + str(item[0]) + "年" + "招生计划为" + str(item[1]) + "人")
                # 查询该年该校招生的类别情况
                sub_sql_string = "SELECT classy,COUNT(*) FROM admission_plan WHERE year = '" + str(item[0]) \
                                 + "' and school = '" + search_school + "' GROUP BY classy;"
                # print(sub_sql_string)
                sub_myresult = mysql_query_sentence(sub_sql_string)
                if len(sub_myresult) == 0:
                    result_edit.append("招生类别查询结果为空！")
                else:
                    for item in sub_myresult:
                        result_edit.append("其中" + str(item[0]) + "招生" + str(item[1]) + "人")
    # 只有专业，统计每年招生人数
    elif search_year == "" and search_school == "" and search_major != "" and search_district == "":
        # 查询该专业各校各年招生总人数
        sql_string = "SELECT year,COUNT(*) FROM admission_plan WHERE major = '" + search_major \
                     + "' GROUP BY year;"
        # print(sql_string)
        myresult = mysql_query_sentence(sql_string)
        if len(myresult) == 0:
            result_edit.append("查询结果为空！")
        else:
            for item in myresult:
                result_edit.append(search_major + str(item[0]) + "招生" + str(item[1]) + "人")
                sub_sql_string = "SELECT school,COUNT(*) FROM admission_plan WHERE major = '" + search_major \
                                 + "'and year = '" + str(item[0]) + "' GROUP BY school;"
                sub_myresult = mysql_query_sentence(sub_sql_string)
                if len(sub_myresult) == 0:
                    result_edit.append("学校具体招生人数查询结果为空！")
                else:
                    for item in sub_myresult:
                        result_edit.append("其中" + str(item[0]) + "招生" + str(item[1]) + "人")
    # 只有地区，统计每年招生人数
    elif search_year == "" and search_school == "" and search_major == "" and search_district != "":
        # 查询该地区各年招生总人数
        sql_string = "SELECT year,COUNT(*) FROM admission_plan WHERE district = '" + search_district \
                     + "' GROUP BY year;"
        myresult = mysql_query_sentence(sql_string)
        if len(myresult) == 0:
            result_edit.append("查询结果为空！")
        else:
            for item in myresult:
                result_edit.append(
                    "C9高校在" + search_district + str(item[0]) + "年" + "招生计划为" + str(item[1]) + "人")
                # 查询该年某校招生的类别情况
                sub_sql_string = "SELECT school,COUNT(*) FROM admission_plan WHERE district = '" \
                                 + search_district + "'and year = '" + str(item[0]) + "' GROUP BY school;"
                # print(sub_sql_string)
                sub_myresult = mysql_query_sentence(sub_sql_string)
                if len(sub_myresult) == 0:
                    result_edit.append("学校具体招生人数查询结果为空！")
                else:
                    for item in sub_myresult:
                        result_edit.append("其中" + str(item[0]) + "招生" + str(item[1]) + "人")
    # 只有年份和学校
    elif search_year != "" and search_school != "" and search_major == "" and search_district == "":
        # 查询学校该年招生总人数
        sql_string = "SELECT COUNT(*) FROM admission_plan WHERE year = '" + search_year \
                     + "' and school = '" + search_school + "' GROUP BY school;"
        myresult = mysql_query_sentence(sql_string)
        if len(myresult) == 0:
            result_edit.append("查询结果为空！")
        else:
            result_edit.append(search_school + search_year + "年" + "招生计划为" + str(myresult[0][0]) + "人")
            sub_sql_string = "SELECT classy,COUNT(*) FROM admission_plan WHERE year = '" + search_year \
                             + "' and school = '" + search_school + "' GROUP BY classy;"
            # print(sub_sql_string)
            sub_myresult = mysql_query_sentence(sub_sql_string)
            if len(sub_myresult) == 0:
                result_edit.append("学校具体招生人数查询结果为空！")
            else:
                for item in sub_myresult:
                    result_edit.append("其中" + str(item[0]) + str(item[1]) + "人")
    # 只有年份和专业
    elif search_year != "" and search_school == "" and search_major != "" and search_district == "":
        # 查询各学校该年该专业招生人数
        sql_string = "SELECT school,COUNT(*) FROM admission_plan WHERE year = '" + search_year \
                     + "' and major = '" + search_major + "' GROUP BY school;"
        myresult = mysql_query_sentence(sql_string)
        if len(myresult) == 0:
            result_edit.append("查询结果为空！")
        else:
            for item in myresult:
                result_edit.append(
                    str(item[0]) + search_year + "年" + search_major + "招生计划为" + str(item[1]) + "人")
    # 只有年份和地区
    elif search_year != "" and search_school == "" and search_major == "" and search_district != "":
        # 查询各学校该年该地区招生人数
        sql_string = "SELECT school,COUNT(*) FROM admission_plan WHERE year = '" + search_year \
                     + "' and district = '" + search_district + "' GROUP BY school;"
        myresult = mysql_query_sentence(sql_string)
        if len(myresult) == 0:
            result_edit.append("查询结果为空！")
        else:
            for item in myresult:
                result_edit.append(
                    str(item[0]) + search_year + "年" + "在" + search_district + "招生计划为" + str(item[1]) + "人")
    # 只有学校和专业
    elif search_year == "" and search_school != "" and search_major != "" and search_district == "":
        # 查询该学校各年该专业招生人数
        sql_string = "SELECT year,COUNT(*) FROM admission_plan WHERE school = '" + search_school \
                     + "' and major = '" + search_major + "' GROUP BY year;"
        myresult = mysql_query_sentence(sql_string)
        if len(myresult) == 0:
            result_edit.append("查询结果为空！")
        else:
            for item in myresult:
                result_edit.append(
                    search_school + str(item[0]) + "年" + search_major + "招生计划为" + str(item[1]) + "人")
    # 只有学校和地区
    elif search_year == "" and search_school != "" and search_major == "" and search_district != "":
        # 查询该学校各年该地区招生人数
        sql_string = "SELECT year,COUNT(*) FROM admission_plan WHERE school = '" + search_school \
                     + "' and district = '" + search_district + "' GROUP BY year;"
        myresult = mysql_query_sentence(sql_string)
        if len(myresult) == 0:
            result_edit.append("查询结果为空！")
        else:
            for item in myresult:
                result_edit.append(search_school + str(item[0]) + "年" + "在" + search_district
                                   + "招生计划为" + str(item[1]) + "人")
    # 只有专业和地区
    elif search_year == "" and search_school == "" and search_major != "" and search_district != "":
        # 查询各年该地区该专业招生人数
        sql_string = "SELECT year,COUNT(*) FROM admission_plan WHERE major = '" + search_major \
                     + "' and district = '" + search_district + "' GROUP BY year;"
        myresult = mysql_query_sentence(sql_string)
        if len(myresult) == 0:
            result_edit.append("查询结果为空！")
        else:
            for item in myresult:
                result_edit.append(
                    str(item[0]) + "年" + search_major + "在" + search_district + "招生计划为" + str(item[1]) + "人")
                # 查询该年各校的招生情况
                sub_sql_string = "SELECT school,COUNT(*) FROM admission_plan WHERE major = '" + search_major \
                                 + "' and district = '" + search_district + "'and year = '" + str(item[0]) \
                                 + "' GROUP BY school;"
                # print(sub_sql_string)
                sub_myresult = mysql_query_sentence(sub_sql_string)
                if len(sub_myresult) == 0:
                    result_edit.append("学校具体招生人数查询结果为空！")
                else:
                    for item in sub_myresult:
                        result_edit.append("其中" + str(item[0]) + "招生" + str(item[1]) + "人")
    # 只有学校、专业、地区
    elif search_year == "" and search_school != "" and search_major != "" and search_district != "":
        # 查询该学校各年该专业该地区招生人数
        sql_string = "SELECT year,COUNT(*) FROM admission_plan WHERE school = '" + search_school \
                     + "' and major = '" + search_major + "' and district = '" + search_district \
                     + "' GROUP BY year;"
        myresult = mysql_query_sentence(sql_string)
        if len(myresult) == 0:
            result_edit.append("查询结果为空！")
        else:
            for item in myresult:
                result_edit.append(search_school + str(item[0]) + "年" + "在" + search_district
                                   + search_major + "招生计划为" + str(item[1]) + "人")
    # 只有年份、专业、地区
    elif search_year != "" and search_school == "" and search_major != "" and search_district != "":
        # 查询各学校该年该专业该地区招生人数
        sql_string = "SELECT school,COUNT(*) FROM admission_plan WHERE year = '" + search_year \
                     + "' and major = '" + search_major + "' and district = '" + search_district \
                     + "' GROUP BY school;"
        myresult = mysql_query_sentence(sql_string)
        if len(myresult) == 0:
            result_edit.append("查询结果为空！")
        else:
            for item in myresult:
                result_edit.append(str(item[0]) + search_year + "年" + "在" + search_district
                                   + search_major + "招生计划为" + str(item[1]) + "人")
    # 只有年份、学校、地区
    elif search_year != "" and search_school != "" and search_major == "" and search_district != "":
        # 查询该学校该年该地区招生人数
        sql_string = "SELECT classy,COUNT(*) FROM admission_plan WHERE year = '" + search_year \
                     + "' and school = '" + search_school + "' and district = '" + search_district \
                     + "' GROUP BY classy;"
        myresult = mysql_query_sentence(sql_string)
        if len(myresult) == 0:
            result_edit.append("查询结果为空！")
        else:
            for item in myresult:
                result_edit.append(search_school + search_year + "年" + "在" + search_district
                                   + "招生" + str(item[0]) + "类" + str(item[1]) + "人")
    # 只有年份、学校、专业
    elif search_year != "" and search_school != "" and search_major != "" and search_district == "":
        # 查询该学校该年该专业招生人数
        sql_string = "SELECT district,COUNT(*) FROM admission_plan WHERE year = '" + search_year \
                     + "' and school = '" + search_school + "' and major = '" + search_major \
                     + "' GROUP BY district;"
        myresult = mysql_query_sentence(sql_string)
        if len(myresult) == 0:
            result_edit.append("查询结果为空！")
        else:
            for item in myresult:
                result_edit.append(search_school + search_year + "年" + search_major
                                   + "在" + str(item[0]) + "招生" + str(item[1]) + "人")
    # 只有年份、学校、专业、地区
    elif search_year != "" and search_school != "" and search_major != "" and search_district != "":
        # 查询该学校该年该专业该地区招生情况
        sql_string = "SELECT classy,COUNT(*) FROM admission_plan WHERE school = '" + search_school \
                     + "' and year = '" + search_year + "' and major = '" + search_major \
                     + "' and district = '" + search_district + "' GROUP BY classy;"
        myresult = mysql_query_sentence(sql_string)
        if len(myresult) == 0:
            result_edit.append("查询结果为空！")
        else:
            for item in myresult:
                result_edit.append(search_school + search_year + "年" + search_major + "在" + search_district
                                   + "招生" + str(item[0]) + "类" + str(item[1]) + "人")
    return result_edit


# 查询admission_score_pro表
def admission_score_pro_table_query(keyword):
    search_table = keyword["search_table"]
    search_year = keyword["search_year"]
    search_school = keyword["search_school"]
    search_major = keyword["search_major"]
    search_district = keyword["search_district"]
    result_edit = []
    # 只有年份
    if search_year != "" and search_school == "" and search_district == "":
        # 查询各学校该年的各地区的录取分数线
        sql_string = "SELECT school FROM admission_score_pro WHERE year = '" + search_year + "' GROUP BY school;"
        myresult = mysql_query_sentence(sql_string)
        if len(myresult) == 0:
            result_edit.append("查询结果为空！")
        else:
            for item in myresult:
                result_edit.append(search_year + "年" + str(item[0]) + "的录取分数如下：")
                # 查询该年各校的录取分数
                sub_sql_string = "SELECT * FROM admission_score_pro WHERE year = '" + search_year \
                                 + "' and school = '" + str(item[0]) + "';"
                # print(sub_sql_string)
                sub_myresult = mysql_query_sentence(sub_sql_string)
                if len(sub_myresult) == 0:
                    result_edit.append(str(item[0]) + "地区录取分数线查询结果为空！")
                else:
                    for item in sub_myresult:
                        result_edit.append(str(item[3]) + str(item[4]) + str(item[5]) + "分数线为" + str(item[6]))
                result_edit.append("\n")
    # 只有学校
    elif search_year == "" and search_school != "" and search_district == "":
        # 查询该学校各年的各地区的录取分数线
        sql_string = "SELECT year FROM admission_score_pro WHERE school = '" + search_school + "' GROUP BY year;"
        myresult = mysql_query_sentence(sql_string)
        if len(myresult) == 0:
            result_edit.append("查询结果为空！")
        else:
            for item in myresult:
                result_edit.append(search_school + str(item[0]) + "年的录取分数如下：")
                # 查询各年该校的录取分数
                sub_sql_string = "SELECT * FROM admission_score_pro WHERE school = '" + search_school \
                                 + "' and year = '" + str(item[0]) + "';"
                # print(sub_sql_string)
                sub_myresult = mysql_query_sentence(sub_sql_string)
                if len(sub_myresult) == 0:
                    result_edit.append(str(item[0]) + "地区录取分数线查询结果为空！")
                else:
                    for item in sub_myresult:
                        result_edit.append(str(item[3]) + str(item[4]) + str(item[5]) + "分数线为" + str(item[6]))
                result_edit.append("\n")
    # 只有地区
    elif search_year == "" and search_school == "" and search_district != "":
        # 查询该地区各年各校的录取分数线
        sql_string = "SELECT year FROM admission_score_pro WHERE district = '" + search_district \
                     + "' GROUP BY year ORDER BY year;"
        myresult = mysql_query_sentence(sql_string)
        if len(myresult) == 0:
            result_edit.append("查询结果为空！")
        else:
            for item in myresult:
                result_edit.append(search_district + str(item[0]) + "年的录取分数如下：")
                # 查询各年该校的录取分数
                sub_sql_string = "SELECT * FROM admission_score_pro WHERE district = '" + search_district \
                                 + "' and year = '" + str(item[0]) + "';"
                # print(sub_sql_string)
                sub_myresult = mysql_query_sentence(sub_sql_string)
                if len(sub_myresult) == 0:
                    result_edit.append(str(item[0]) + "地区录取分数线查询结果为空！")
                else:
                    for item in sub_myresult:
                        result_edit.append(str(item[1]) + str(item[4]) + str(
                            item[5]) + "分数线为" + str(item[6]))
                result_edit.append("\n")
    # 只有年份、学校
    elif search_year != "" and search_school != "" and search_district == "":
        # 查询该年该学校各地区的录取分数线
        result_edit.append(search_school + search_year + "年的录取分数如下：")
        sql_string = "SELECT * FROM admission_score_pro WHERE year = '" + search_year \
                     + "' and school = '" + search_school + "';"
        # print(sub_sql_string)
        myresult = mysql_query_sentence(sql_string)
        if len(myresult) == 0:
            result_edit.append(search_school + search_year + "年地区录取分数线查询结果为空！")
        else:
            for item in myresult:
                result_edit.append(str(item[3]) + str(item[4]) + str(
                    item[5]) + "分数线为" + str(item[6]))
        result_edit.append("\n")
    # 只有年份、地区
    elif search_year != "" and search_school == "" and search_district != "":
        # 查询该年该地区各学校的录取分数线
        result_edit.append(search_district + search_year + "年的录取分数如下：")
        sql_string = "SELECT * FROM admission_score_pro WHERE year = '" + search_year \
                     + "' and district = '" + search_district + "';"
        # print(sub_sql_string)
        myresult = mysql_query_sentence(sql_string)
        if len(myresult) == 0:
            result_edit.append(search_district + search_year + "年录取分数线查询结果为空！")
        else:
            for item in myresult:
                result_edit.append(str(item[1]) + str(item[4]) + str(
                    item[5]) + "分数线为" + str(item[6]))
        result_edit.append("\n")
    # 只有学校、地区
    elif search_year == "" and search_school != "" and search_district != "":
        # 查询该学校该地区各年的录取分数线
        result_edit.append(search_school + "在" + search_district + "的历年录取分数如下：")
        sql_string = "SELECT * FROM admission_score_pro WHERE  school =  '" + search_school \
                     + "' and district = '" + search_district + "';"
        # print(sub_sql_string)
        myresult = mysql_query_sentence(sql_string)
        if len(myresult) == 0:
            result_edit.append(search_school + "在" + search_district + "的历年录取分数线查询结果为空！")
        else:
            for item in myresult:
                result_edit.append(str(item[2]) + str(item[4]) + str(
                    item[5]) + "分数线为" + str(item[6]))
        result_edit.append("\n")
    # 只有年份、学校、地区
    elif search_year != "" and search_school != "" and search_district != "":
        # 查询该学校该地区该年的录取分数线
        result_edit.append(search_year + search_school + "在" + search_district + "的录取分数如下：")
        sql_string = "SELECT * FROM admission_score_pro WHERE  year = '" + search_year \
                     + "' and school =  '" + search_school \
                     + "' and district = '" + search_district + "';"
        # print(sub_sql_string)
        myresult = mysql_query_sentence(sql_string)
        if len(myresult) == 0:
            result_edit.append(search_year + search_school + "在" + search_district + "的录取分数线查询结果为空！")
        else:
            for item in myresult:
                result_edit.append(str(item[4]) + str(item[5]) + "分数线为" + str(item[6]))
        result_edit.append("\n")
    return result_edit


# 查询admission_score_major表
def admission_score_major_table_query(keyword):
    search_table = keyword["search_table"]
    search_year = keyword["search_year"]
    search_school = keyword["search_school"]
    search_major = keyword["search_major"]
    search_district = keyword["search_district"]
    result_edit = []
    # 只有年份
    # 只有学校
    # 只有专业
    if search_year == "" and search_school == "" and search_major != "" and search_district == "":
        # 查询各年各学校各地区该专业录取分数线
        sql_string = "SELECT year FROM admission_score_major WHERE major = '" + search_major \
                     + "' GROUP BY year;"
        myresult = mysql_query_sentence(sql_string)
        if len(myresult) == 0:
            result_edit.append("查询结果为空！")
        else:
            for year_item in myresult:
                result_edit.append(str(year_item[0]) + "年" + search_major + "专业的录取分数如下：")
                # 查询该年各校各地区该专业的录取分数
                sub_sql_string = "SELECT school FROM admission_score_major WHERE major = '" + search_major \
                                 + "' and year = '" + str(year_item[0]) + "' GROUP BY school;"
                # print(sub_sql_string)
                sub_myresult = mysql_query_sentence(sub_sql_string)
                if len(sub_myresult) == 0:
                    result_edit.append(str(year_item[0]) + "年" + search_major + "专业录取分数线查询结果为空！")
                else:
                    for school_item in sub_myresult:
                        result_edit.append(str(school_item[0]) + search_major + "专业的录取分数如下：")
                        # 查询该年该校各地区该专业的录取分数
                        sub_sub_sql_string = "SELECT * FROM admission_score_major WHERE major = '" + search_major \
                                             + "' and year = '" + str(year_item[0]) \
                                             + "' and school = '" + str(school_item[0]) + "';"
                        # print(sub_sql_string)
                        sub_sub_myresult = mysql_query_sentence(sub_sub_sql_string)
                        if len(sub_sub_myresult) == 0:
                            result_edit.append(str(year_item[0]) + "年" + str(school_item[0])
                                               + search_major + "专业录取分数线查询结果为空！")
                        else:
                            for item in sub_sub_myresult:
                                result_edit.append(
                                    str(item[2]) + str(item[5]) + "类" + "最高分：" + str(item[6]) + ";\t平均分：" + str(item[7]) + ";\t最低分：" + str(
                                        item[8]))
                            result_edit.append("\n")
                    result_edit.append("\n")
            result_edit.append("\n")
    # 只有地区
    # 只有年份、学校
    # 只有年份、专业
    elif search_year != "" and search_school == "" and search_major != "" and search_district == "":
        # 查询该年各校各地区该专业的录取分数
        sql_string = "SELECT school FROM admission_score_major WHERE major = '" + search_major \
                         + "' and year = '" + search_year + "' GROUP BY school;"
        # print(sql_string)
        myresult = mysql_query_sentence(sql_string)
        if len(myresult) == 0:
            result_edit.append(search_year + "年" + search_major + "专业录取分数线查询结果为空！")
        else:
            for school_item in myresult:
                result_edit.append(search_year + str(school_item[0]) + search_major + "专业的录取分数如下：")
                # 查询该年该校各地区该专业的录取分数
                sub_sql_string = "SELECT * FROM admission_score_major WHERE major = '" + search_major \
                                     + "' and year = '" + search_year \
                                     + "' and school = '" + str(school_item[0]) + "';"
                # print(sub_sql_string)
                sub_myresult = mysql_query_sentence(sub_sql_string)
                if len(sub_myresult) == 0:
                    result_edit.append(search_year + "年" + str(school_item[0])
                                       + search_major + "专业录取分数线查询结果为空！")
                else:
                    for item in sub_myresult:
                        result_edit.append(
                            str(item[2]) + str(item[5]) + "类" + "最高分：" + str(item[6]) + ";\t平均分：" + str(item[7]) + ";\t最低分：" + str(
                                item[8]))
                    result_edit.append("\n")
        result_edit.append("\n")
    # 只有年份、地区
    # 只有学校、专业
    elif search_year == "" and search_school != "" and search_major != "" and search_district == "":
        # 查询各年该学校各地区该专业录取分数线
        sql_string = "SELECT year FROM admission_score_major WHERE major = '" + search_major \
                     + "' and school = '" + search_school+ "' GROUP BY year;"
        myresult = mysql_query_sentence(sql_string)
        if len(myresult) == 0:
            result_edit.append("查询结果为空！")
        else:
            for year_item in myresult:
                result_edit.append(str(year_item[0]) + "年" + search_major + "专业的录取分数如下：")
                # 查询该年该校各地区该专业的录取分数
                sub_sql_string = "SELECT * FROM admission_score_major WHERE major = '" + search_major \
                                     + "' and year = '" + str(year_item[0]) \
                                     + "' and school = '" + search_school + "';"
                # print(sub_sql_string)
                sub_myresult = mysql_query_sentence(sub_sql_string)
                if len(sub_myresult) == 0:
                    result_edit.append(str(year_item[0]) + "年" + search_school
                                       + search_major + "专业录取分数线查询结果为空！")
                else:
                    for item in sub_myresult:
                        result_edit.append(
                            str(item[2]) + str(item[5]) + "类" + "最高分：" + str(item[6]) + ";\t平均分：" + str(item[7]) + ";\t最低分：" + str(
                                item[8]))
                    result_edit.append("\n")
            result_edit.append("\n")
        result_edit.append("\n")
    # 只有学校、地区
    # 只有专业、地区
    elif search_year == "" and search_school == "" and search_major != "" and search_district != "":
        # 查询各年各学校该地区该专业录取分数线
        sql_string = "SELECT year FROM admission_score_major WHERE major = '" + search_major \
                     + "' and district = '"+ search_district + "' GROUP BY year;"
        myresult = mysql_query_sentence(sql_string)
        if len(myresult) == 0:
            result_edit.append("查询结果为空！")
        else:
            for year_item in myresult:
                result_edit.append(str(year_item[0]) + "年" + search_major + "专业的录取分数如下：")
                # 查询该年各校该地区该专业的录取分数
                sub_sql_string = "SELECT * FROM admission_score_major WHERE major = '" + search_major \
                                     + "' and year = '" + str(year_item[0]) \
                                     + "' and district = '" + search_district + "';"
                # print(sub_sql_string)
                sub_myresult = mysql_query_sentence(sub_sql_string)
                if len(sub_myresult) == 0:
                    result_edit.append(str(year_item[0]) + "年" + search_major + "在"+search_district + "的录取分数查询为空：")
                else:
                    for item in sub_myresult:
                        result_edit.append(
                            str(item[1]) + str(item[5]) + "类" + "最高分：" + str(item[6]) + ";\t平均分：" + str(item[7]) + ";\t最低分：" + str(
                                item[8]))
                    result_edit.append("\n")
            result_edit.append("\n")
        result_edit.append("\n")
    # 只有学校、专业、地区
    elif search_year == "" and search_school != "" and search_major != "" and search_district != "":
        # 查询各年该校该地区该专业的录取分数
        result_edit.append(search_school + search_major + "在" + search_district + "的录取分数如下：")
        sql_string = "SELECT * FROM admission_score_major WHERE major = '" + search_major \
                         + "' and school = '" + search_school \
                         + "' and district = '" + search_district + "';"
        # print(sql_string)
        myresult = mysql_query_sentence(sql_string)
        if len(myresult) == 0:
            result_edit.append(search_school + search_major + "在" + search_district + "的录取分数查询为空：")
        else:
            for item in myresult:
                result_edit.append(str(item[3]) + "年" + str(item[5]) + "类" + "最高分："
                                   + str(item[6]) + ";\t平均分：" + str(item[7]) + ";\t最低分：" + str(item[8]))
            result_edit.append("\n")
    # 只有年份、专业、地区
    elif search_year != "" and search_school == "" and search_major != "" and search_district != "":
        # 查询各校该年该地区该专业的录取分数
        result_edit.append(search_year + search_major + "在" + search_district + "的录取分数如下：")
        sql_string = "SELECT * FROM admission_score_major WHERE major = '" + search_major \
                     + "' and year = '" + search_year \
                     + "' and district = '" + search_district + "';"
        # print(sql_string)
        myresult = mysql_query_sentence(sql_string)
        if len(myresult) == 0:
            result_edit.append(search_year + search_major + "在" + search_district + "的录取分数查询为空：")
        else:
            for item in myresult:
                result_edit.append(str(item[1]) + str(item[5]) + "类" + "最高分："
                                   + str(item[6]) + ";\t平均分：" + str(item[7]) + ";\t最低分：" + str(item[8]))
            result_edit.append("\n")
    # 只有年份、学校、地区
    # 只有年份、学校、专业
    elif search_year != "" and search_school != "" and search_major != "" and search_district == "":
        # 查询该校该年各地区该专业的录取分数
        result_edit.append(search_school + search_year + search_major + "的录取分数如下：")
        sql_string = "SELECT * FROM admission_score_major WHERE major = '" + search_major \
                     + "' and year = '" + search_year \
                     + "' and school = '" + search_school + "';"
        # print(sql_string)
        myresult = mysql_query_sentence(sql_string)
        if len(myresult) == 0:
            result_edit.append(search_school + search_year + search_major + "的录取分数查询为空：")
        else:
            for item in myresult:
                result_edit.append(str(item[2]) + str(item[5]) + "类" + "最高分："
                                   + str(item[6]) + ";\t平均分：" + str(item[7]) + ";\t最低分：" + str(item[8]))
            result_edit.append("\n")
    # 只有年份、学校、专业、地区
    elif search_year != "" and search_school != "" and search_major != "" and search_district != "":
        # 查询该校该年该地区该专业的录取分数
        result_edit.append(search_school + search_year + search_major +"在" + search_district + "的录取分数如下：")
        sql_string = "SELECT * FROM admission_score_major WHERE major = '" + search_major \
                     + "' and year = '" + search_year + "' and district = '" + search_district\
                     + "' and school = '" + search_school + "';"
        # print(sql_string)
        myresult = mysql_query_sentence(sql_string)
        if len(myresult) == 0:
            result_edit.append(search_school + search_year + search_major + "在" + search_district + "的录取分数查询为空：")
        else:
            for item in myresult:
                result_edit.append(str(item[5]) + "类" + "最高分："
                                   + str(item[6]) + ";\t平均分：" + str(item[7]) + ";\t最低分：" + str(item[8]))
            result_edit.append("\n")
    return result_edit


# 测试模块
if __name__ == '__main__':
    print("start...")
