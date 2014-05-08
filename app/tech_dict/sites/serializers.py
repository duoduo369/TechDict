#coding: utf-8

from rest_framework import serializers, fields

from sites.models import SiteRawData, KeyWordCN, KeyWordEN


class SiteRawDataSeri(serializers.ModelSerializer):

    subject = serializers.CharField()

    class Meta:
        model = SiteRawData

class KeyWordENSeri(serializers.ModelSerializer):

    raw_data = SiteRawDataSeri()

    class Meta:
        model = KeyWordEN

    def transform_raw_data(self, obj, value):
        attrs = ('id', 'title_en', 'subject_id', 'subject', 'url')
        result = []
        for each in value:
            result.append({attr: each[attr] for attr in attrs})
        return result

class KeyWordCNSeri(serializers.ModelSerializer):

    raw_data = SiteRawDataSeri()

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
