# -*- coding: utf-8 -*-
import os
import sys

# 本配置文件地址
SCRAPY_SETTINGS_PATH = os.path.realpath(__file__)

# 找到相对路径加入sys.path中
# 本项目django路径 '.../TechDict/app/tech_dict'
# scrapy setting文件路径 '.../TechDict/app/spiders/spiders/settings.py'
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

# 下载器超时时间(单位: 秒)
DOWNLOAD_TIMEOUT = 20

# 下载延迟
# http://scrapy-chs.readthedocs.org/zh_CN/latest/topics/practices.html
# 设置下载延迟(2或更高)。参考 DOWNLOAD_DELAY 设置
DOWNLOAD_DELAY = 0.8
# 如果启用，当从相同的网站获取数据时，Scrapy将会等待一个随机的值
# 使用0.5到1.5之间的一个随机值 * DOWNLOAD_DELAY 的结果作为等待间隔
RANDOMIZE_DOWNLOAD_DELAY = True

# 自动限速(AutoThrottle)扩展
# http://scrapy-chs.readthedocs.org/zh_CN/latest/topics/autothrottle.html
AUTOTHROTTLE_ENABLED = True

LOG_LEVEL = 'INFO'
LOG_FILE = 'log/paper_edu.log'

# 禁用cookie
COOKIES_ENABLED = False
