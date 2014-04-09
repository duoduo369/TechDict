# -*- coding: utf-8 -*-
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import Selector
from spiders.items import PaperEduItem

class PaperEduSpider(CrawlSpider):
    name = 'paper_edu_spider'
    allowed_domains = ['paper.edu.cn',]
    start_urls = [
        u''
    ]
