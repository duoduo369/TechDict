#coding: utf-8
from __future__ import absolute_import
from rest_framework import serializers, fields
from tech_dict.serializers import DynamicFieldsModelSerializer

from sites.models import SiteRawData, KeyWordCN, KeyWordEN


class SiteRawDataSeri(DynamicFieldsModelSerializer):

    subject = serializers.CharField()

    class Meta:
        model = SiteRawData

class KeyWordENSeri(DynamicFieldsModelSerializer):

    raw_data = SiteRawDataSeri()
    raw_data_count = serializers.IntegerField()

    class Meta:
        model = KeyWordEN

    def transform_raw_data(self, obj, value):
        attrs = ('id', 'title_en', 'subject_id', 'subject', 'url')
        result = []
        for each in value:
            result.append({attr: each[attr] for attr in attrs})
        return result

class KeyWordCNSeri(DynamicFieldsModelSerializer):

    raw_data = SiteRawDataSeri()
    raw_data_count = serializers.IntegerField()

    class Meta:
        model = KeyWordCN

    def transform_raw_data(self, obj, value):
        attrs = ('id', 'title_cn', 'subject_id', 'subject', 'url')
        result = []
        for each in value:
            result.append({attr: each[attr] for attr in attrs})
        return result

class KeyWordENRelationSeri(KeyWordENSeri):
    trans = KeyWordCNSeri()

class KeyWordCNRelationSeri(KeyWordCNSeri):
    trans = KeyWordENSeri()

    def transform_trans(self, obj, value):
        for each in value:
            del each['cn_word']
        return value
