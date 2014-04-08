# -*- coding: utf-8 -*-
# Scrapy settings for spiders project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

import os
import sys
# 本配置文件地址
SCRAPY_SETTINGS_PATH = os.path.realpath(__file__)
# django根目录地址，默认是settings上面3级
DJANGO_PATH_UP_LEVEL = 3
DJANGO_PROJECT_NAME = 'tech_dict'
# django 配置文件地址
_p = SCRAPY_SETTINGS_PATH
for i in xrange(DJANGO_PATH_UP_LEVEL):
    _p = os.path.split(_p)[0]

DJANGO_PROJECT_PATH = os.path.join(_p, DJANGO_PROJECT_NAME)
sys.path.insert(0, DJANGO_PROJECT_PATH)
os.environ['DJANGO_SETTINGS_MODULE'] = DJANGO_PROJECT_NAME + '.settings'
BOT_NAME = 'spiders'

SPIDER_MODULES = ['spiders.spiders']
NEWSPIDER_MODULE = 'spiders.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'spiders (+http://www.yourdomain.com)'
