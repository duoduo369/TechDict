# -*- coding: utf-8 -*-
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.contrib.djangoitem import DjangoItem
import misc.log as log

class DjangoPipeline(object):

    def process_item(self, item, spider):
        if isinstance(item, DjangoItem):
            item.save()
        return item
