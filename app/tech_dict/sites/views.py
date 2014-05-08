from __future__ import absolute_import
from sites.models import KeyWordCN, KeyWordEN
from sites.serializers import KeyWordCNRelationSeri, KeyWordENRelationSeri
from tech_dict.views import BaseView
from tech_dict.custom_exceptions import ArgumentError, MISSING_FIELD
from rest_framework import status
from rest_framework.response import Response

class SearchView(BaseView):

    def get_param(self, request):
        data = request.GET
        attrs = ('word', 'subject')
        return {attr: data.get(attr, None) for attr in attrs}

    def get(self, request):
        params = self.get_param(request)
        word = params['word']
        if not word:
            raise ArgumentError(MISSING_FIELD)
        result = KeyWordCN.objects.filter(word__contains=word)
        serilizer = KeyWordCNRelationSeri(result, many=True)
        #result = KeyWordEN.objects.filter(word__contains=word)
        #serilizer = KeyWordENRelationSeri(result, many=True)
        return Response(serilizer.data)
