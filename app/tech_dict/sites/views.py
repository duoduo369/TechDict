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

def filter_seri_data(data, subject_id=None,
      raw_data_num=7, trans_num=7, trans_raw_data_num=7):
    '''过滤不该出现的数据'''
    # 先截断
    for each in data:
        each['trans'] = each['trans'][:trans_num]
        each['raw_data'] = each['raw_data'][:raw_data_num]
        for trans in each['trans']:
            trans['raw_data'] = trans['raw_data'][:trans_raw_data_num]
    # 后过滤
    if subject_id:
        for each in data:
            for trans in each['trans']:
                trans['raw_data'] = [raw for raw in trans['raw_data'] \
                 if raw['subject_id'] == subject_id][:trans_raw_data_num]

    return [each for each in data if each['raw_data']]

def sorted_raw_data(data):
    '''
        排序seri中的raw_data列表
    '''
    return sorted(data, key=itemgetter('weight'), reverse=True)

def top_n(n=10, subject_id=None, cut_filed=True):
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
            annotate(raw_data_count=Count('raw_data')).\
            order_by('-raw_data_count')[:n]
        _ids = (op(each) for each in ids)
        result = Model.objects.filter(~Q(word=''), id__in=_ids)
        if cut_filed:
            serilizer = Seri(result, many=True,
                             exclude_fields=('raw_data','trans', 'cn_word'))
            seri_data.extend(serilizer.data)
        else:
            serilizer = Seri(result, many=True)
            seri_data.extend(serilizer.data)
            seri_data = filter_seri_data(seri_data, subject_id=subject_id)
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
        param = {attr: data.get(attr, None) for attr in attrs}
        # fix 前端空格会变成+的bug
        if param['word'] and '+' in param['word']:
            param['word'] = param['word'].replace('+', ' ')
        return param

    def sorted_result(self, result):
        '''将查询结果排序'''
        # 将结果按照元数据条数排序
        result = sorted(result, key=attrgetter('raw_data_count', 'word'), reverse=True)
        return result

    def sorted_seri_data(self, result):
        '''
            排序原始数据
            因为django query many to many不能set
            需要在seri中排序外键的原始数据
            model中使用trans排序
        '''
        for each in result:
            each['raw_data'] = sorted_raw_data(each['raw_data'])
            for trans in each['trans']:
                trans['raw_data'] = sorted_raw_data(trans['raw_data'])

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
        data = self.sorted_seri_data(data)
        return Response(data)

class WordCloudView(BaseView):

    def get(get, request):
        return Response(top_n(150))
