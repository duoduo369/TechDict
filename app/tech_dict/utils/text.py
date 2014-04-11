# -*- coding: utf-8 -*-
import re

PATTERN_CN_SEMICOLON = re.compile(u'；')
PATTERN_EN_SEMICOLON = re.compile(u';')

def split(raw_str, pattern):
    '''
        arguments:
            raw_str -- 原始字符串
            pattern -- 正则分隔符号
        return:
            分割后的list或者None

    '''
    if raw_str:
        raw_str = raw_str.strip()
        if raw_str:
            return map(unicode.strip, re.split(pattern, raw_str))
    return []
