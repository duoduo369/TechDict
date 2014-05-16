#coding: utf-8
from __future__ import absolute_import
from rest_framework import serializers, fields
from tech_dict.serializers import DynamicFieldsModelSerializer
from operator import itemgetter

from sites.models import SiteRawData, KeyWordCN, KeyWordEN


class SiteRawDataSeri(DynamicFieldsModelSerializer):

    subject = serializers.CharField()

    class Meta:
        model = SiteRawData

class KeyWordSeriBase(DynamicFieldsModelSerializer):

    raw_data = SiteRawDataSeri()
    raw_data_count = serializers.IntegerField()

    def transform_raw_data(self, obj, value):
        attrs = ('id', 'title_cn', 'title_en', 'subject_id', 'subject', 'url')
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


class KeyWordRelationMixin(object):

    def transform_trans(self, obj, value):
        options = self.extra_options
        if options and 'subject_id' in options:
            subject_id = options['subject_id']
            for data in value:
                data['raw_data'] = [raw for raw in data['raw_data'] \
                        if raw['subject_id'] == subject_id]
        return value


def soreted_raw_data(result):
    '''返回排序中的'''
    result = sorted(result, key=itemgetter('title_cn'), reverse=True)
    return result


class KeyWordENRelationSeri(KeyWordENSeri, KeyWordRelationMixin):

    trans = KeyWordCNSeri()

    def transform_raw_data(self, obj, value):
        value = super(KeyWordENRelationSeri, self).transform_raw_data(obj, value)
        options = self.extra_options
        if options and 'subject_id' in options:
            subject_id = options['subject_id']
            value = [raw for raw in value if raw['subject_id'] == subject_id]
        value = soreted_raw_data(value)
        return value


class KeyWordCNRelationSeri(KeyWordCNSeri, KeyWordRelationMixin):

    trans = KeyWordENSeri()

    def transform_raw_data(self, obj, value):
        value = super(KeyWordCNRelationSeri, self).transform_raw_data(obj, value)
        options = self.extra_options
        if options and 'subject_id' in options:
            subject_id = options['subject_id']
            value = [raw for raw in value if raw['subject_id'] == subject_id]
        value = soreted_raw_data(value)
        return value
