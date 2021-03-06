
from scrapy import log

def warn(msg):
    log.msg(str(msg), level=log.WARNING)


def info(msg):
    log.msg(str(msg), level=log.INFO)


def debug(msg):
    log.msg(str(msg), level=log.DEBUG)

def error(msg):
    log.msg(str(msg), level=log.ERROR)

def critical(msg):
    log.msg(str(msg), level=log.CRITICAL)
