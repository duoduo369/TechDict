# -*- coding: utf-8 -*-
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

DOWNLOADER_MIDDLEWARES = {
    'spiders.misc.middleware.CustomHttpProxyMiddleware': 400,
    'spiders.misc.middleware.CustomUserAgentMiddleware': 401,
    'spiders.misc.middleware.CustomNextPageMiddleware': 402,
}

ITEM_PIPELINES = {
    'spiders.pipelines.DjangoPipeline': 300,
}

# 下载延迟
DOWNLOAD_DELAY = 0.15

LOG_LEVEL = 'INFO'
LOG_FILE = 'log/paper_edu.log'

# 禁用cookie
COOKIES_ENABLED = False
