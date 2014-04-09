# -*- coding: utf-8 -*-
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor as sle
from scrapy.selector import Selector
from spiders.items import PaperEduItem
import spiders.misc.log as log

class PaperEduSpider(CrawlSpider):
    name = 'paper_edu_spider'
    allowed_domains = ['paper.edu.cn',]
    rules = (
        Rule(
            sle(
                allow=('/index.php/default/releasepaper/content/\d+',),
                #restrict_xpaths=('//*[@id="right"]/span[@class="zm_text_jh"]/a',),
            ),
            callback='parse_content',
        ),
        Rule(
            sle(
                allow=("\?type=0.*page=\d+",),
                restrict_xpaths=('//*[@id="right"]/li[@class="zm_gjss_right_l1"]/li/a[4]',),
            ),
            follow=True,
            callback='parse_list',
        ),
    )

    def __init__(self, start_date=None, end_date=None, per_pages=20, page=1):
        super(PaperEduSpider, self).__init__()
        url = (u'http://www.paper.edu.cn/advanced_search/resultHighSearch?'
        'type=0&subject=&title=&author=&abstract=&keywords=&'
        'begin=%s&end=%s&y1=2014&m1=04&d1=02&y2=2014&m2=04&d2=09&'
        'star=&method=RELEVANCE&filename=&company=&language=0&'
        'p1=0&p2=0&p3=0&p4=0&p5=0&p6=0&r1=and&r2=and&r3=and&r4=and&r5=and&'
        'pagesize=%s&timeA=&userleft=&paperleft=&jiaocha=&1=1&page=%s',)[0]
        start_url = url % (start_date, end_date, per_pages, page)
        self.start_urls = [start_url]
        print '=========='
        print self.start_urls
        print self.rules

    def parse_start_url(self, response):
        log.info('start url parse_content')
        log.info(response.url)

    def parse_content(self, response):
        log.info('parse_content')
        log.info(response.url)

    def parse_list(self, response):
        log.info('parse_list')
        log.info(response.url)

