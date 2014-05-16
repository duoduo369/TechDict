# -*- coding: utf-8 -*-
from __future__ import absolute_import

from django.db.models import Count, Q
from rest_framework import status
from rest_framework.response import Response
from operator import itemgetter, attrgetter
import model_settings as config
from sites.models import KeyWordCN, KeyWordEN
from sites.serializers import KeyWordCNRelationSeri, KeyWordENRelationSeri
from tech_dict.custom_exceptions import ArgumentError, MISSING_FIELD
from tech_dict.views import BaseView
from utils.language import detect_language

SUBJECT_ID = config.SUBJECT_ID

# 根据语言检测，通过配置返回对应结果
KEYWORD_MAPPER = {
    'zh': {
        'keyword_model': KeyWordCN,
        'keyword_seri': KeyWordCNRelationSeri,
    },
    'en': {
        'keyword_model': KeyWordEN,
        'keyword_seri': KeyWordENRelationSeri,
    }
}

MAX_RESULT = 50

def filter_seri_data(data):
    '''过滤不该出现的数据'''
    return [each for each in data if each['raw_data']]


def top_n(n=None, subject_id=None, cut_filed=True):
    '''
        返回关键词表中最热的n条记录，n * len(KEYWORD_MAPPER)条

        subject_id -- 科目代码，过滤
        cut_filed -- seri中是否cut字段，词云中使用True
    '''
    op = itemgetter('id')
    seri_data = []
    for each in KEYWORD_MAPPER.itervalues():
        Model = each['keyword_model']
        Seri = each['keyword_seri']
        ids = Model.objects.values('id').\
            annotate(raw_data_count=Count('raw_data'))
        if n:
            ids = ids[:n]
        _ids = (op(each) for each in ids)
        result = Model.objects.filter(~Q(word=''), id__in=_ids)
        if cut_filed:
            serilizer = Seri(result, many=True,
                             exclude_fields=('raw_data','trans', 'cn_word'))
            seri_data.extend(serilizer.data)
        else:
            if subject_id:
                serilizer = Seri(result, many=True,
                        extra_options=dict(subject_id=subject_id))
            else:
                serilizer = Seri(result, many=True)
            seri_data.extend(serilizer.data)
            seri_data = filter_seri_data(seri_data)
    return sorted(seri_data, key=itemgetter('raw_data_count'), reverse=True)

class SearchView(BaseView):

    def get_param(self, request):
        '''
            word -- 查询关键词
            subject -- 分类
            maxResults -- 返回结果最多条数
        '''
        data = request.GET
        attrs = ('word', 'subject', 'maxResults')
        return {attr: data.get(attr, None) for attr in attrs}

    def sorted_result(self, result):
        '''将查询结果排序'''
        result = sorted(result, key=attrgetter('raw_data_count', 'word'), reverse=True)
        return result

    def get(self, request):
        params = self.get_param(request)
        word = params['word']
        subject = params['subject']
        max_results = params['maxResults']
        max_results = MAX_RESULT if not max_results else max_results
        subject_id = None
        if subject and subject in SUBJECT_ID:
            subject_id = SUBJECT_ID[subject]
        if not word:
            if subject_id:
                return Response(top_n(n=60,subject_id=subject_id,
                    cut_filed=False))
            else:
                return Response(top_n(20, cut_filed=False))
        query_args = {'word__icontains': word,}
        if subject_id:
            query_args['raw_data__subject_id'] = subject_id
        # 语言检测
        language = detect_language(word)
        _Model = KEYWORD_MAPPER[language]['keyword_model']
        _Seri = KEYWORD_MAPPER[language]['keyword_seri']
        result = _Model.objects.filter(**query_args)[:max_results]
        result = self.sorted_result(result)
        if subject_id:
            serilizer = _Seri(result, many=True,
                    extra_options=dict(subject_id=subject_id))
        else:
            serilizer = _Seri(result, many=True)
        data = filter_seri_data(serilizer.data)
        return Response(data)

class WordCloudView(BaseView):

    def get(get, request):
        return Response(top_n(150))
