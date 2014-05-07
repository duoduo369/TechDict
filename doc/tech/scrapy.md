scrapy相关
===

.
├── spiders
│   ├── scrapy.cfg
│   └── spiders
│       ├── __init__.py
│       ├── __init__.pyc
│       ├── items.py
│       ├── pipelines.py
│       ├── settings.py
│       ├── settings.pyc
│       └── spiders
│           ├── __init__.py
│           └── __init__.pyc
....

开启shell调试
---
    在spiders目录下
    scrapy shell

配置django
---
    需要在scrapy的settings.py中添加环境变量

    sys.path.insert(0, DJANGO_PROJECT_PATH)
    os.environ['DJANGO_SETTINGS_MODULE'] = DJANGO_PROJECT_NAME + '.settings'

抓取命名
---
    scrapy crawl paper_edu_spider -a start_date=2014-03-01 -a end_date=2014-03-10
