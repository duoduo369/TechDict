# -*- coding: utf-8 -*-
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor as sle
from scrapy.contrib.loader import ItemLoader
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.selector import Selector

import spiders.misc.log as log
from spiders.items import PaperEduItem
from paper_edu.models import PaperEduRaw

URL_PREFIX = u'http://www.paper.edu.cn/advanced_search/resultHighSearch'

class PaperEduSpider(CrawlSpider):
    name = 'paper_edu_spider'
    allowed_domains = ['paper.edu.cn',]
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

    def __init__(self, start_date=None, end_date=None, per_pages=20, page=1):
        '''
            arguments:
                start_date -- 2014-01-01
                end_date -- 2014-01-02
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

    def parse_start_url(self, response):
        '''
            处理start url第一页
        '''
        log.info('start url parse_content')
        log.info(response.url)

    def parse_content(self, response):
        log.info(response.url)
        paper_edu_raw = PaperEduRaw.objects.filter(url=response.url)
        # 抓过的不在重抓
        if paper_edu_raw:
            return
        loader = ItemLoader(item=PaperEduItem(), response=response)
        loader.add_value('url', response.url)
        loader.add_value('raw_html', response.body)
        item = loader.load_item()
        for attr, value in item.iteritems():
            if isinstance(value, list):
                item[attr] = ''.join(value)
        return item
