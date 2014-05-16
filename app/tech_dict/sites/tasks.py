# -*- coding: utf-8 -*-
from __future__ import absolute_import
from logging import getLogger

from celery.task import task

from sites.models import KeyWordCN, KeyWordEN, SiteRawData
from utils.dateutil import parse_dates, today, yesterday
from utils.text import PATTERN_EN_SEMICOLON, split

logger = getLogger('sites')

KEYWORD_MODELS = (KeyWordCN, KeyWordEN)

def _stat_keyword_relation(raw_data, keywords_cns, keywords_ens):
    '''分析中英文词的对应关系'''
    assert isinstance(raw_data, SiteRawData)
    if len(keywords_ens) != len(keywords_cns):
        logger.exception(u'中文英文关键字个数对应错误，查看此数据\nraw id:%s\nurl:%s',
                raw_data.id, raw_data.url)
        return
    keywords = zip(keywords_cns, keywords_ens)
    for word_cn, word_en in keywords:
        pe_word_cn = KeyWordCN.objects.get_or_create(word=word_cn)[0]
        pe_word_en = KeyWordEN.objects.get_or_create(word=word_en)[0]
        pe_word_cn.raw_data.add(raw_data)
        pe_word_en.raw_data.add(raw_data)
        pe_word_en.cn_word.add(pe_word_cn)

def update_keyword_raw_data_count():
    '''更新关键词中的raw_data_count'''
    for Model in KEYWORD_MODELS:
        for keyword in Model.objects.all():
            keyword.raw_data_count = keyword.raw_data.count()

@task
def classification(start_date=None, end_date=None, stat_yesterday=False, stat_all=False):
    '''
        默认分析今天数据
        start_yesterday -- 分析昨天数据
        stat_all -- 分析全部数据
        start_date -- 分析start_date数据
        start_date ~ end_date 分析 start_date <= date <= end_date的数据
        优先级: 今天 < start_yesterday < start_date[, end_date] < stat_all
        默认今天
    '''
    raw_data = None
    # 默认分析今天数据
    # 获得起止日期
    count_date_start = today()
    count_date_end = count_date_start
    if stat_yesterday:
        count_date_start = yesterday()
        count_date_end = count_date_start
    if start_date:
        if end_date:
            count_date_start, count_date_end = parse_dates((start_date, end_date))
        else:
            count_date_start, count_date_end = parse_dates((start_date,
                start_date))
    # 获得原始数据
    if stat_all:
        raw_data = SiteRawData.objects.filter()
    else:
        raw_data = SiteRawData.objects.filter(
            pub_date__gte=count_date_start,
            pub_date__lte=count_date_end,
        )
    for raw in raw_data:
        keywords_cns = split(raw.keywords_cn, PATTERN_EN_SEMICOLON)
        keywords_ens = split(raw.keywords_en, PATTERN_EN_SEMICOLON)
        _stat_keyword_relation(raw, keywords_cns, keywords_ens)

    # 最后更新keyword_raw_data
    update_keyword_raw_data_count()
