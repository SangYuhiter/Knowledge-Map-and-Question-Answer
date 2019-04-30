# -*- coding: utf-8 -*-
"""
@File  : TemplateAnswerQuestion.py
@Author: SangYu
@Date  : 2019/3/27 15:07
@Desc  : 模板方法回答问题
"""
from Log.Logger import MyLog
from QuestionAnalysis.QuestionPretreatment import (question_segment_hanlp, question_abstract,
                                                   question_analysis_to_keyword, question_keyword_normalize,
                                                   find_question_match_template)
from TemplateLoad.QuestionTemplate import (build_mysql_string_by_template_and_keymap,
                                           build_mysql_answer_string_by_template)
from InformationGet.MysqlOperation import mysql_query_sentence


# 传入问题使用模板回答问题
def answer_question_by_template(question: str, school_flag: int = 0, school_name: str = "")->(dict, list):
    """
    分词-》提取关键词、抽象问句-》抽象问句匹配模板-》模板构造sql语句-》sql语句返回查询结果-》查询结果构造模板输出
    :param question: 问题
    :param school_flag 学校标志位，是否指定默认学校
    :param school_name 指定的默认学校名
    :return: 中间结果词典，最终答案列表
    """
    # 保存中间结果
    mid_result = {}
    segment_list = question_segment_hanlp(question)
    mid_result["segment_list"] = segment_list
    ab_question = question_abstract(segment_list)
    mid_result["ab_question"] = ab_question
    keyword = question_analysis_to_keyword(segment_list)
    # 修改默认学校名
    if school_flag:
        keyword["search_school"] = school_name
    mid_result["keyword"] = keyword
    keyword_normalize = question_keyword_normalize(keyword)
    mid_result["keyword_normalize"] = keyword_normalize
    template_sentence_type = keyword_normalize["search_table"]
    fq_condition, fq_target, match_template_question, match_template_answer \
        = find_question_match_template(ab_question, template_sentence_type)
    # 修改模板框
    if school_flag:
        if "(school)" not in match_template_question:
            match_template_question = "(school)"+match_template_question
    mid_result["match_template_question"] = match_template_question
    mid_result["match_template_answer"] = match_template_answer
    mysql_string = build_mysql_string_by_template_and_keymap(match_template_question, template_sentence_type,
                                                             keyword_normalize)
    mid_result["mysql_string"] = mysql_string
    # 数据库查询
    result = []
    result_edit = []
    if mysql_string == "":
        result_edit.append("问句条件词为空，无法构建查询语句！")
    else:
        # 若只有学校一个关键词
        if "and" not in mysql_string:
            result_edit.append("问句条件词只有学校，查询过宽！")
        else:
            result = mysql_query_sentence(mysql_string)
            if len(result) == 0:
                result_edit.append("查询结果为空！")
            else:
                mid_result["search_result"] = result
                for item in result:
                    answer_string = build_mysql_answer_string_by_template(match_template_answer, item)
                    result_edit.append(answer_string)
    return mid_result, result_edit


if __name__ == '__main__':
    main_logger = MyLog(logger=__name__).getlog()
    main_logger.info("start...")
    test_question = "哈工大前年软件工程石家庄招生人数？"
    main_logger.debug(test_question)
    test_mid_result, test_result = answer_question_by_template(test_question)
    for mid in test_mid_result:
        main_logger.debug(str(mid)+":"+str(test_mid_result[mid]))
    main_logger.debug("查询结果：")
    for result in test_result:
        main_logger.debug(str(result))
    main_logger.info("end...")
