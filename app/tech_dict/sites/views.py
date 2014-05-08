# -*- coding: utf-8 -*-
from __future__ import absolute_import
import model_settings as config
from sites.models import KeyWordCN, KeyWordEN
from sites.serializers import KeyWordCNRelationSeri, KeyWordENRelationSeri
from tech_dict.views import BaseView
from tech_dict.custom_exceptions import ArgumentError, MISSING_FIELD
from rest_framework import status
from rest_framework.response import Response
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

class SearchView(BaseView):

    def get_param(self, request):
        data = request.GET
        attrs = ('word', 'subject')
        return {attr: data.get(attr, None) for attr in attrs}

    def get(self, request):
        params = self.get_param(request)
        word = params['word']
        subject = params['subject']
        if not word:
            raise ArgumentError(MISSING_FIELD)
        query_args = {'word__contains': word,}
        if subject and subject in SUBJECT_ID:
            query_args['raw_data__subject_id'] = SUBJECT_ID[subject]
        # 语言检测
        language = detect_language(word)
        _Model = KEYWORD_MAPPER[language]['keyword_model']
        _Seri = KEYWORD_MAPPER[language]['keyword_seri']
        result = _Model.objects.filter(**query_args)
        serilizer = _Seri(result, many=True)
        return Response(serilizer.data)
