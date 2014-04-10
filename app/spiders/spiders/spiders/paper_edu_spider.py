# -*- coding: utf-8 -*-
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor as sle
from scrapy.contrib.loader import ItemLoader
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.selector import Selector

import spiders.misc.log as log
from spiders.items import PaperEduItem

URL_PREFIX = u'http://www.paper.edu.cn/advanced_search/resultHighSearch'

class PaperEduSpider(CrawlSpider):
    name = 'paper_edu_spider'
    allowed_domains = ['paper.edu.cn',]
    _CSS = {
        'authors_cn': '#right > div.grid_10.omega.alpha > div.w794 >\
                div:nth-child(2) > span::text',
        'locations_cn': '#right > div.grid_10.omega.alpha > div.w794 >\
                div:nth-child(3) > span::text',
        'title_cn': '#right > div.grid_10.omega.alpha > div.r_two >\
                div > h1 > p::text',
        'authors_en': '#right > div.grid_10.omega.alpha > div.w794 >\
                div:nth-child(5) > span::text',
        'locations_en': '#right > div.grid_10.omega.alpha > div.w794 >\
                div:nth-child(6) > span::text',
        'title_en': '#right > div.grid_10.omega.alpha > div.r_two >\
                div > h2 > p::text',
    }
    _XPATH = {
        'abstract_cn': '//*[@id="right"]/div[2]/div[2]/div[4]/text()[2]',
        'keywords_cn': '//*[@id="right"]/div[2]/div[2]/div[4]/text()[3]',
        'abstract_en': '//*[@id="right"]/div[2]/div[2]/div[7]/text()[2]',
        'keywords_en': '//*[@id="right"]/div[2]/div[2]/div[7]/text()[3]',
    }
    _JOIN = {
        'url': '',
        'raw_html': '',
        'authors_cn': ',',
        'authors_en': ',',
        'keywords_cn': ',',
        'keywords_en': ',',
        'abstract_cn': '',
        'abstract_en': '',
        'locations_cn': '',
        'locations_en': '',
        'title_en': '',
        'title_cn': '',
        'title_en': '',
    }
    rules = (
        Rule(
            sle(
                allow=('/index.php/default/releasepaper/content/\d+',),
            ),
            callback='parse_content',
        ),
        Rule(
            sle(
                allow=("\?type=0.*page=\d+.*",),
                restrict_xpaths=(
                    u'//a[re:match(text(), "下一页")]',
                ),
            ),
            follow=True,
        ),
    )

    def __init__(self, start_date=None, end_date=None,
                 per_pages=20, page=1, refetch=True):
        '''
            arguments:
                start_date <= date <= end_date
                start_date -- 2014-01-01 起始日期
                end_date -- 2014-01-02 截止日期
                per_pages -- 20 每页显示条数
                refetch -- 是否重抓已存在的数据
        '''
        super(PaperEduSpider, self).__init__()
        url = (
         URL_PREFIX +
        '?type=0&subject=&title=&author=&abstract=&keywords=&'
        'begin=%s&end=%s&y1=2014&m1=04&d1=02&y2=2014&m2=04&d2=09&'
        'star=&method=RELEVANCE&filename=&company=&language=0&'
        'p1=0&p2=0&p3=0&p4=0&p5=0&p6=0&r1=and&r2=and&r3=and&r4=and&r5=and&'
        'pagesize=%s&timeA=&userleft=&paperleft=&jiaocha=&1=1&page=%s',)[0]
        start_url = url % (start_date, end_date, per_pages, page)
        self.start_urls = [start_url]
        self.refetch = refetch
        self._Model = PaperEduItem.django_model

    def parse_start_url(self, response):
        '''
            处理start url第一页
        '''
        log.info('start url parse_content')
        log.info(response.url)

    def parse_content(self, response):
        log.info(response.url)
        django_istance = self._Model.objects.filter(url=response.url)
        # django obj之前存在,并且不重抓则忽略此条
        if django_istance and not self.refetch:
            return
        if django_istance:
            # 重抓此数据
            django_istance.delete()
        loader = ItemLoader(item=PaperEduItem(), response=response)
        # parse page
        loader.add_value('url', response.url)
        loader.add_value('raw_html', response.body)
        for attr, css in self._CSS.iteritems():
            loader.add_css(attr, css)
        for attr, xpath in self._XPATH.iteritems():
            loader.add_xpath(attr, xpath)

        item = loader.load_item()

        # transe attr
        for attr, value in item.iteritems():
            if isinstance(value, list):
                item[attr] = self._JOIN.get(attr, '').join(value)
        return item
