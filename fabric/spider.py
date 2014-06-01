#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
date format: yyyy-MM-dd : 2014-01-01

Usage:
    spider.py <start_date> <end_date>

'''
from docopt import docopt
from fabric.api import *

env.roledefs = {
    'online61': ['deployer@shizilukou.cn',],
    #'online61': ['deployer@115.28.11.182',],
}

COMAND = 'ls -l | wc'
ENABLE_PYTHON_ENV_CMD = 'source /opt/python_env/django1.6.1/bin/activate'

@roles('online61')
def test_remote(a=1, b=2):
    print a, b
    run(COMAND)

@roles('online61')
def scrapy(start_date, end_date):
    cd_cmd = 'cd /opt/TechDict/app/spiders'
    scrapy_cmd = 'scrapy crawl paper_edu_spider -a start_date={start_date} -a end_date={end_date}'.format(
            start_date=start_date, end_date=end_date)
    cmd = '{python_env_cmd} && {cd_cmd} && {scrapy_cmd}'.format(
            python_env_cmd=ENABLE_PYTHON_ENV_CMD,
            cd_cmd=cd_cmd,
            scrapy_cmd=scrapy_cmd
    )
    print scrapy_cmd
    run(cmd)

if __name__ == '__main__':
    arguments = docopt(__doc__, version='duoduo 1.0')
    start_date = arguments['<start_date>']
    end_date = arguments['<end_date>']
    execute(scrapy, start_date, end_date)
