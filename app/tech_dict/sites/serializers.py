#coding: utf-8
from __future__ import absolute_import
from rest_framework import serializers, fields
from tech_dict.serializers import DynamicFieldsModelSerializer
from operator import itemgetter

from sites.models import SiteRawData, KeyWordCN, KeyWordEN, StatRawData


class SiteRawDataSeri(DynamicFieldsModelSerializer):

    subject = serializers.CharField()

    class Meta:
        model = SiteRawData

class KeyWordSeriBase(DynamicFieldsModelSerializer):

    raw_data = SiteRawDataSeri()
    raw_data_count = serializers.IntegerField()

    def transform_raw_data(self, obj, value):
        attrs = ('id', 'title_cn', 'title_en', 'subject_id',
                 'subject', 'url', 'weight')
        result = []
        for each in value:
            result.append({attr: each[attr] for attr in attrs})
        return result


class KeyWordENSeri(KeyWordSeriBase):

    class Meta:
        model = KeyWordEN


class KeyWordCNSeri(KeyWordSeriBase):

    class Meta:
        model = KeyWordCN


class KeyWordENRelationSeri(KeyWordENSeri):

    trans = KeyWordCNSeri()


class KeyWordCNRelationSeri(KeyWordCNSeri):

    trans = KeyWordENSeri()

class StatRawDataSeri(DynamicFieldsModelSerializer):

    class Meta:
        model = StatRawData
