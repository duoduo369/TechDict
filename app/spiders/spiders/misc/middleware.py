# -*- coding: utf-8 -*-
import random
import re

from . import log
from scrapy.http import Request
from twisted.internet.error import TCPTimedOutError

from agents import AGENTS
from proxy import PROXIES

PAGE_PATTERN = re.compile(u'page=(\d+)')

class CustomHttpProxyMiddleware(object):

    def process_request(self, request, spider):
        # TODO implement complex proxy providing algorithm
        if self.use_proxy(request):
            p = random.choice(PROXIES)
            try:
                request.meta['proxy'] = "http://%s" % p['ip_port']
            except Exception, e:
                log.critical("Exception {msg}".format(msg=e))

    def use_proxy(self, request):
        """
        using direct download for depth <= 2
        using proxy with probability 0.3
        """
        if "depth" in request.meta and int(request.meta['depth']) <= 2:
            return False
        i = random.randint(1, 10)
        return i <= 2


class CustomUserAgentMiddleware(object):
    def process_request(self, request, spider):
        agent = random.choice(AGENTS)
        request.headers['User-Agent'] = agent


class CustomNextPageMiddleware(object):

    def process_exception(self, request, exception, spider):
        '''处理下一页异常断抓的问题'''
        url = request.url
        log.error("Exception {msg}\nurl: {url}".format(msg=exception, url=url))
        if isinstance(exception, TCPTimedOutError):
            if 'advanced_search' in url:
                s = PAGE_PATTERN.search(url)
                if s and s.groups():
                    next_page = int(s.groups()[0]) + 1
                    next_url = re.sub(
                        PAGE_PATTERN,'page={page}'.format(page=next_page),
                        url,
                    )
                    return Request(next_url)
