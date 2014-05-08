#coding: utf-8

from rest_framework import serializers, fields

from sites.models import KeyWordCN


class KeyWordCNSeri(serializers.ModelSerializer):

    class Meta:
        model = KeyWordCN
