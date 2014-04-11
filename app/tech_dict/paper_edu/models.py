# -*- coding: utf-8 -*-
from django.db import models
import model_settings as config

MAX_LENGTH_20 = config.MAX_LENGTH_20
MAX_LENGTH_100 = config.MAX_LENGTH_100
MAX_LENGTH_200 = config.MAX_LENGTH_200
MAX_LENGTH_1024 = config.MAX_LENGTH_1024

class PaperEduRaw(models.Model):
    '''
        中国科技论文在线

        从中华科技论文在线抓回的原始数据
        cn & en字段:
            title -- 标题
            authors -- 作者
            locations -- 单位
            abstract -- 摘要
            keywords -- 关键字
        其余字段
            pub_date -- 发布时间
            impressions -- 浏览量
            collections -- 收藏数
            comments -- 评论数
            pdf_download -- pdf下载链接
            author_intro -- 作者简介
            contact -- 通信联系人
            paper_edu_pub_record -- 收录情况中国科技论文在线
            pub_periodical -- 发表期刊
            url -- 抓取页面链接
            created_at 记录创建日期
            updated_at 记录更新日期
            raw_html
    '''
    title_cn = models.CharField(
        verbose_name=u'标题_中',
        max_length=MAX_LENGTH_200,
        blank=True,
        null=True,
    )

    title_en = models.CharField(
        verbose_name=u'标题_英',
        max_length=MAX_LENGTH_200,
        blank=True,
        null=True,
    )
    authors_cn = models.CharField(
        verbose_name=u'作者_中',
        max_length=MAX_LENGTH_200,
        blank=True,
        null=True,
    )
    authors_en = models.CharField(
        verbose_name=u'作者_英',
        max_length=MAX_LENGTH_1024,
        blank=True,
        null=True,
    )
    locations_cn = models.CharField(
        verbose_name=u'单位_中',
        max_length=MAX_LENGTH_1024,
        blank=True,
        null=True,
    )
    locations_en = models.CharField(
        verbose_name=u'单位_英',
        max_length=MAX_LENGTH_200,
        blank=True,
        null=True,
    )
    abstract_cn = models.TextField(
        verbose_name=u'摘要_中',
        blank=True,
        null=True,
    )
    abstract_en = models.TextField(
        verbose_name=u'摘要_英',
        blank=True,
        null=True,
    )
    keywords_cn = models.CharField(
        verbose_name=u'关键字_中',
        max_length=MAX_LENGTH_200,
        blank=True,
        null=True,
    )
    keywords_en = models.CharField(
        verbose_name=u'关键字_英',
        max_length=MAX_LENGTH_200,
        blank=True,
        null=True,
    )
    pub_date = models.DateField(
        verbose_name=u'发布日期',
        blank=True,
        null=True,
    )
    impressions = models.IntegerField(
        verbose_name=u'浏览量',
        default=0,
    )
    collections = models.IntegerField(
        verbose_name=u'收藏数',
        default=0,
    )
    comments = models.IntegerField(
        verbose_name=u'评论数',
        default=0,
    )
    pdf_download = models.URLField(
        verbose_name=u'pdf下载链接',
        blank=True,
        null=True,
    )
    author_intro = models.CharField(
        verbose_name=u'作者简介',
        max_length=MAX_LENGTH_200,
        blank=True,
        null=True,
    )
    contact = models.CharField(
        verbose_name=u'通信联系人',
        max_length=MAX_LENGTH_200,
        blank=True,
        null=True,
    )
    paper_edu_pub_record = models.CharField(
        verbose_name=u'中国科技在线收录情况',
        max_length=MAX_LENGTH_200,
        blank=True,
        null=True,
    )
    pub_periodical = models.CharField(
        verbose_name=u'发表期刊',
        max_length=MAX_LENGTH_200,
        blank=True,
        null=True,
    )
    url = models.URLField(
        verbose_name=u'抓取页面链接',
        unique=True,
    )
    raw_html = models.TextField(
        verbose_name=u'源代码',
        blank=True,
        null=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class PaperEduKeyWordCN(models.Model):
    '''中文关键字'''
    word = models.CharField(
        verbose_name=u'中文关键词',
        max_length=MAX_LENGTH_100,
        unique=True,
    )
    raw_data = models.ManyToManyField(
        'paper_edu.PaperEduRaw',
        verbose_name=u'原始抓取数据',
    )
    def __unicode__(self):
        return self.word

class PaperEduKeyWordEN(models.Model):
    '''英文关键字'''
    word = models.CharField(
        verbose_name=u'英文关键词',
        max_length=MAX_LENGTH_100,
        unique=True,
    )
    raw_data = models.ManyToManyField(
        'paper_edu.PaperEduRaw',
        verbose_name=u'原始抓取数据',
    )
    cn_word = models.ManyToManyField(
        'paper_edu.PaperEduKeyWordCN',
        verbose_name=u'中文关键字',
    )
    def __unicode__(self):
        return self.word
