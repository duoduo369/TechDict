# -*- coding: utf-8 -*-
from __future__ import absolute_import
from logging import getLogger

from celery.task import task

from sites.models import KeyWordCN, KeyWordEN, SiteRawData
from utils.dateutil import parse_dates, today, yesterday
from utils.text import PATTERN_EN_SEMICOLON, PATTERN_EN_COMMA, split
from model_settings import KEY_WORD_TYPE, KEY_WORD_TYPE_ID, KEY_WORD_TYPE_COEFFICIENT
logger = getLogger('sites')

KEYWORD_MODELS = (KeyWordCN, KeyWordEN)

def get_keywords(raw_data, keyword_type='keyword'):
    '''根据原始类型获得'''
    assert keyword_type in KEY_WORD_TYPE
    if keyword_type == 'keyword':
        keywords_cns = split(raw_data.keywords_cn, PATTERN_EN_SEMICOLON)
        keywords_ens = split(raw_data.keywords_en, PATTERN_EN_SEMICOLON)
    elif keyword_type == 'author':
        keywords_cns = split(raw_data.authors_cn, PATTERN_EN_COMMA)
        keywords_ens = split(raw_data.authors_en, PATTERN_EN_COMMA)
    result = dict(
        keyword_type=KEY_WORD_TYPE_ID[keyword_type],
        keywords_cns=keywords_cns,
        keywords_ens=keywords_ens,
    )
    return result

def _stat_keyword_relation(raw_data, keyword_type):
    '''
        分析中英文词的对应关系
        数据比较大的时候cpu飙升，速达慢
    '''
    assert isinstance(raw_data, SiteRawData)
    keyword_dict = get_keywords(raw_data, keyword_type)
    keywords_cns = keyword_dict['keywords_cns']
    keywords_ens = keyword_dict['keywords_ens']
    keyword_type = keyword_dict['keyword_type']
    if len(keywords_ens) != len(keywords_cns):
        logger.exception(u'中文英文关键字个数对应错误，查看此数据\nraw id:%s\nurl:%s',
                raw_data.id, raw_data.url)
        return
    keywords = zip(keywords_cns, keywords_ens)
    for word_cn, word_en in keywords:
        pe_word_cn = KeyWordCN.objects.get_or_create(word=word_cn)[0]
        pe_word_en = KeyWordEN.objects.get_or_create(word=word_en)[0]
        if pe_word_cn.keyword_type != keyword_type:
            pe_word_cn.keyword_type = keyword_type
            pe_word_en.keyword_type = keyword_type
            pe_word_cn.save()
            pe_word_en.save()
        pe_word_cn.raw_data.add(raw_data)
        pe_word_en.raw_data.add(raw_data)
        pe_word_en.cn_word.add(pe_word_cn)

@task
def update_keyword_raw_data_count(keyword_type=None):
    '''
        更新关键词中的raw_data_count
    '''
    query_args = {}
    if keyword_type in KEY_WORD_TYPE:
        query_args['keyword_type'] = KEY_WORD_TYPE_ID['keyword_type']
    for Model in KEYWORD_MODELS:
        index = 0
        total = Model.objects.count()
        data = Model.objects.filter(**query_args)
        for keyword in data:
            raw_data_count = keyword.raw_data.count()
            if raw_data_count != keyword.raw_data_count:
                keyword.raw_data_count = raw_data_count
                keyword.save()
            index += 1
            print 'Model:', Model, 'total:', total, ' now:', index

def get_raw_data(start_date=None, end_date=None, stat_yesterday=False, stat_all=False):
    '''
        工具方法，根据日期条件获得raw_data列表
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
        ).order_by('pub_date')

    return raw_data

@task
def classification(
        start_date=None, end_date=None, stat_yesterday=False,
        stat_all=False, keyword_type='keyword'):
    assert keyword_type in KEY_WORD_TYPE
    '''
        默认分析今天数据
        start_yesterday -- 分析昨天数据
        stat_all -- 分析全部数据
        start_date -- 分析start_date数据
        start_date ~ end_date 分析 start_date <= date <= end_date的数据
        优先级: 今天 < start_yesterday < start_date[, end_date] < stat_all
        默认今天
    '''
    raw_data = get_raw_data(start_date, end_date, stat_yesterday, stat_all)
    index = 0
    total = len(raw_data)
    for raw in raw_data:
        print raw.pub_date, raw.url
        _stat_keyword_relation(raw, keyword_type)
        index+=1
        print 'total:', total, ' now:', index

@task
def update_raw_data_weight(
        start_date=None, end_date=None, stat_yesterday=False, stat_all=False):
    raw_data = get_raw_data(start_date, end_date, stat_yesterday, stat_all)
    index = 0
    total = len(raw_data)

    for raw in raw_data:
        print raw.pub_date, raw.url
        # keywords_cns count = keywords_ens count
        weight = 0
        for each in KEY_WORD_TYPE_COEFFICIENT.itervalues():
            # 得到不同类型的关键词
            data_set = (
                 raw.keywordcn_set.filter(keyword_type=each['id']),
                 raw.keyworden_set.filter(keyword_type=each['id'])
            )
            # 此类型关键词的系数
            k = each['coefficient']
            # 每一个词用系数乘以raw_data_count
            for each in data_set:
                for _keyword in each:
                    weight += k * _keyword.raw_data_count

        if raw.weight != weight:
            raw.weight = weight
            raw.save()
        index+=1
        print 'total:', total, ' now:', index
