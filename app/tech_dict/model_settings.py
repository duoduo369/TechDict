#!/usr/bin/env python
# -*- coding: utf-8 -*-

# django model字段
MAX_LENGTH_20 = 20
MAX_LENGTH_100 = 100
MAX_LENGTH_200 = 200
MAX_LENGTH_1024 = 1024

# 抓取站点的site_id
SITE_PAPER_EDU = 1 # http://www.paper.edu.cn/ 中国科技在线

# 所有论文分类
SUBJECTS = (
    u'default', u'数学', u'信息科学与系统科学', u'力学', u'物理学',
    u'化学', u'天文学', u'地球科学', u'生物学', u'农学', u'林学',
    u'畜牧、兽医科学', u'水产学', u'基础医学', u'临床医学',
    u'军事医学与特种医学', u'预防医学与卫生学', u'药学', u'中医学与中药学',
    u'工程与技术科学基础学科', u'测绘科学技术', u'材料科学',
    u'矿山工程技术', u'冶金工程技术', u'机械工程', u'动力与电气工程',
    u'能源科学技术', u'核科学技术', u'电子、通信与自动控制技术',
    u'计算机科学技术', u'化学工程', u'纺织科学技术', u'食品科学技术',
    u'土木建筑工程', u'水利工程', u'交通运输工程', u'航空航天科学技术',
    u'环境科学技术', u'安全科学技术', u'管理学', u'经济学',
    u'图书馆、情报与文献学', u'教育学', u'体育科学', u'交叉学科专题',
)

# 论文分类
# 学科:id
SUBJECT_ID = {sub:i for i,sub in enumerate(SUBJECTS)}

# 论文分类反查
# id:学科
ID_SUBJECT = {i:sub for i,sub in enumerate(SUBJECTS)}

# 关键词类型
KEY_WORD_TYPE  = ('keyword', 'author')
KEY_WORD_TYPE_ID = {t:i for i,t in enumerate(KEY_WORD_TYPE)}
ID_KEY_WORD_TYPE = {i:t for i,t in enumerate(KEY_WORD_TYPE)}
