# -*- coding: utf-8 -*-
from paper_edu.models import PaperEduRaw, PaperEduKeyWordCN, PaperEduKeyWordEN
from utils.dateutil import parse_dates
from utils.text import split, PATTERN_EN_SEMICOLON
from logging import getLogger

logger = getLogger('paper_edu')

def classification(start_date=None, end_date=None, stat_all=False):
    raw_data = None
    if stat_all:
        raw_data = PaperEduRaw.objects.filter()
    else:
        start_date, end_date = parse_dates((start_date, end_date))
        raw_data = PaperEduRaw.objects.filter(
            pub_date__gte=start_date,
            pub_date__lt=end_date,
        )
    for raw in raw_data:
        keywords_cns = split(raw.keywords_cn, PATTERN_EN_SEMICOLON)
        keywords_ens = split(raw.keywords_en, PATTERN_EN_SEMICOLON)
        _classification(raw, keywords_cns, keywords_ens)


def _classification(raw_data, keywords_cns, keywords_ens):
    assert isinstance(raw_data, PaperEduRaw)
    if len(keywords_ens) != len(keywords_cns):
        logger.exception(u'中文英文关键字个数对应错误，查看此数据\nraw id:%s\nurl:%s',
                raw_data.id, raw_data.url)
        return
    keywords = zip(keywords_cns, keywords_ens)
    for word_cn, word_en in keywords:
        pe_word_cn = PaperEduKeyWordCN.objects.get_or_create(word=word_cn)[0]
        pe_word_en = PaperEduKeyWordEN.objects.get_or_create(word=word_en)[0]
        pe_word_cn.raw_data.add(raw_data)
        pe_word_en.raw_data.add(raw_data)
        pe_word_en.cn_word.add(pe_word_cn)
