# -*- coding: utf-8 -*-
import re
from datetime import datetime

from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor as sle
from scrapy.contrib.loader import ItemLoader
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.http import Request
from scrapy.selector import Selector

import spiders.misc.log as log
from spiders.misc.utils import str_to_date, date_to_str, range_date
from spiders.items import PaperEduItem
import model_settings as config

SITE_PAPER_EDU = config.SITE_PAPER_EDU
SUBJECT_ID = config.SUBJECT_ID

URL_PREFIX = u'http://www.paper.edu.cn/advanced_search/resultHighSearch'
SEMICOLON_PATTERN = re.compile(u'[;；]')
REDIRECT_PATTERN = re.compile('(/html/releasepaper/((\d+)/)*)')
REDIRECT_PATTERN_2 = re.compile('(/releasepaper/content/(\d+-)*\d+)')

class PaperEduSpider(CrawlSpider):
    name = 'paper_edu_spider'
    allowed_domains = ['paper.edu.cn',]
    PUB_DATE_FORMAT = "%Y-%m-%d"
    # type: (0,全部), (1, 首发)
    _TYPE = 1
    _CSS = {
        'authors_cn': '#right > div.grid_10.omega.alpha > div.w794 >\
                div:nth-child(2) > span::text',
        'locations_cn': '#right > div.grid_10.omega.alpha > div.w794 >\
                div:nth-child(3) > span::text',
        'title_cn': '#right > div.grid_10.omega.alpha > div.r_two >\
                div.cmtdiv .title_02::text',
        'authors_en': '#right > div.grid_10.omega.alpha > div.w794 >\
                div:nth-child(5) > span::text',
        'locations_en': '#right > div.grid_10.omega.alpha > div.w794 >\
                div:nth-child(6) > span::text',
        'title_en': '#right > div.grid_10.omega.alpha > div.r_two >\
                div.cmtdiv .title_03::text',
        'impressions': '#paper_visitnum::text',
        'collections': '#paper_collectnum::text',
        'comments': '#paper_comment::text',
        'pdf_download': '#right > div.grid_10.omega.alpha > div.w794 >\
                div:nth-child(8) > a::attr(href)'
    }
    _XPATH = {
        'abstract_cn': '//*[@id="right"]/div[2]/div[2]/div[4]/text()[2]',
        'keywords_cn': '//*[@id="right"]/div[2]/div[2]/div[4]/text()[4]',
        'abstract_en': '//*[@id="right"]/div[2]/div[2]/div[7]/text()[2]',
        'keywords_en': '//*[@id="right"]/div[2]/div[2]/div[7]/text()[4]',
        'author_intro': '//*[@id="right"]/div[2]/div[2]/div[9]/div/text()[2]',
        'contact': '//*[@id="right"]/div[2]/div[2]/div[9]/div/text()[3]',
        'paper_edu_pub_record': '//*[@id="right"]/div[2]/div[2]/div[10]/div/text()[2]',
        'pub_periodical': '//*[@id="right"]/div[2]/div[2]/div[10]/div/text()[4]',
    }
    _XPATH_CORRECTION = {
        'keywords_cn': '//*[@id="right"]/div[2]/div[2]/div[4]/text()[3]',
        'keywords_en': '//*[@id="right"]/div[2]/div[2]/div[7]/text()[3]',
    }
    _REPLACE = {
        'keywords_cn': (SEMICOLON_PATTERN, u';'),
        'keywords_en': (re.compile(u'[;；,，]'), u';'),
        'locations_cn': (SEMICOLON_PATTERN, u';'),
        'locations_en': (SEMICOLON_PATTERN, u';'),
    }
    _SPLIT_AND_JOIN = {
        'keywords_cn': (re.compile(u'\s+'), u';', lambda s: u';' not in s),
    }
    _JOIN = {
        'authors_cn': ',',
        'authors_en': ',',
        'keywords_cn': ',',
        'keywords_en': ',',
        'pdf_download': ',',
    }
    rules = (
        Rule(
            sle(
                allow=('/index.php/default/releasepaper/content/\d+',),
            ),
            callback='redirect_request',
        ),
        Rule(
            sle(
                allow=('/html/releasepaper/((\d+)/)*',),
            ),
            callback='parse_content',
        ),

        Rule(
            sle(
                allow=("\?type=\d+.*page=\d+.*",),
                restrict_xpaths=(
                    u'//a[re:match(text(), "下一页")]',
                ),
            ),
            follow=True,
        ),
    )

    def __init__(self, start_date=None, end_date=None,
                 per_pages=10, page=1, refetch=False):
        '''
            arguments:
                start_date <= date <= end_date
                start_date -- 2014-01-01 起始日期
                end_date -- 2014-01-02 截止日期
                per_pages -- 10 每页显示条数,不要设置太大减少超时时间
                refetch -- 是否重抓已存在的数据
        '''
        super(PaperEduSpider, self).__init__()
        url = (
          URL_PREFIX +
          '?type={_type}&begin={begin}&end={end}&method=RELEVANCE&'
          'language=0&p1=0&p2=0&p3=0&p4=0&p5=0&p6=0&r1=and&r2=and&'
          'r3=and&r4=and&r5=and&pagesize={pagesize}&page={page}',
        )[0]
        s_date, e_date = str_to_date(start_date), str_to_date(end_date)
        self.start_urls =[]
        for d in range_date(s_date, e_date):
            one_date = date_to_str(d)
            self.start_urls.append(url.format(
                _type=self._TYPE, begin=one_date, end=one_date,
                pagesize=per_pages, page=page,
            ))
        self.refetch = refetch
        self._Model = PaperEduItem.django_model

    def parse_start_url(self, response):
        '''
            处理start url第一页
        '''
        #url = response.url
        #log.info('start url: {url}'.format(url=url))

    def parse_content(self, response):
        django_istance = self._Model.objects.filter(url=response.url)
        # django obj之前存在,并且不重抓则忽略此条
        if django_istance and not self.refetch:
            return
        if django_istance:
            # 重抓此数据
            django_istance.delete()
        sel = Selector(response)
        loader = ItemLoader(item=PaperEduItem(), response=response)
        # parse page
        loader.add_value('url', response.url)
        raw_html = None
        try:
            raw_html = response.body_as_unicode()
        except:
            raw_html = response.body.decode('latin-1')
        loader.add_value('raw_html', raw_html)
        for attr, css in self._CSS.iteritems():
            loader.add_css(attr, css)
        for attr, xpath in self._XPATH.iteritems():
            loader.add_xpath(attr, xpath)

        pub_css = '#right > div.grid_10.omega.alpha > div.r_two > div.cmtdiv .tip'
        tip = sel.css(pub_css)
        pub_date = tip.re(u'发布时间：\s*(\d+-\d+-\d+)')

        item = loader.load_item()
        # 特殊字段处理

        # 站点标识
        item['site_id'] = SITE_PAPER_EDU

        # 分类标识
        title = sel.css('title::text').extract()[0]
        subject = title.split(' - ')[1]
        item['subject_id'] = SUBJECT_ID.get(subject, -1)

        # keywords页面不规范
        for attr, xpath_correction in self._XPATH_CORRECTION.iteritems():
            if not ''.join(item.get(attr, '')).strip(' ;\n'):
                item[attr] = sel.xpath(xpath_correction).extract()[0]

        try:
            pub_date = pub_date[0]
            pub_date = datetime.strptime(pub_date, self.PUB_DATE_FORMAT).date()
        except IndexError:
            pub_date = None
        except ValueError:
            pub_date = None
        item['pub_date'] = pub_date

        # transe attr
        for attr, value in item.iteritems():
            if isinstance(value, list):
                item[attr] = self._JOIN.get(attr, '').join(value)

        # 字段替换,例如替换关键字中文逗号等
        for attr,_r in self._REPLACE.iteritems():
            old, new = _r
            item[attr] = re.sub(old, new, item[attr])

        # 不规则页面元素替换，关键词中有使用空格切分和;切分的
        for attr, _r in self._SPLIT_AND_JOIN.iteritems():
            pattern, join_str, judge_func = _r
            if judge_func(item[attr]):
                item[attr] = join_str.join(re.split(pattern, item[attr]))

        return item

    def redirect_request(self, response):
        '''网站改版，旧网页变成重定向'''
        _url = 'http://www.paper.edu.cn{url}'
        try:
            url = _url.format(url=REDIRECT_PATTERN.search(response.body).group())
        except AttributeError:
            url = _url.format(url=REDIRECT_PATTERN_2.search(response.body).group())
        yield Request(url=url, callback=self.parse_content)


class PaperEduSpiderOnePage(PaperEduSpider):

    name = 'paper_edu_spider_one_page'
    rules = (
        Rule(
            sle(
                allow=('/index.php/default/releasepaper/content/\d+',),
            ),
            callback='parse_content',
        ),
    )

    def __init__(self, url, refetch=False):
        CrawlSpider.__init__(self)
        self.start_urls = [url]

    def parse_start_url(self, response):
        self.parse_content(response)
