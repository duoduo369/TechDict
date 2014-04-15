# -*- coding: utf-8 -*-
from datetime import datetime
from dateutil.rrule import rrule, DAILY

YMD_FORMAT = '%Y-%m-%d'

def str_to_date(_str, _format=YMD_FORMAT):
    return datetime.strptime(_str, _format)

def date_to_str(date, _format=YMD_FORMAT):
    return date.strftime(_format)

def range_date(start_date, end_date, freq=DAILY):
    for date in rrule(freq, dtstart=start_date, until=end_date):
        yield date
