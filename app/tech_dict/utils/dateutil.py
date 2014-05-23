# -*- coding: utf-8 -*-

from  django.utils.dateparse import parse_date
from datetime import datetime, timedelta

def parse_dates(iter_item):
    '''
        iter_item -- ['2014-04-01',...]
        format -- 2014-04-01
    '''
    return map(parse_date, iter_item)

def today():
    '''
        return today -- type/date
    '''
    return datetime.now().date()

def yesterday():
    '''
        return yesterday -- type/date
    '''
    return today() - timedelta(days=1)


def date_to_string(date, format='%Y-%m-%d'):
    return date.strftime(format)


def next_year(year):
    '''
        year -- int
    '''
    return datetime(year+1, 1, 1) + timedelta(1)
