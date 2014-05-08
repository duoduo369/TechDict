# -*- coding: utf-8 -*-
from __future__ import absolute_import
from guess_language import guessLanguage

def detect_language(text):
    '''
        语言检测，text需要为unicode
        返回en或zh
    '''
    _text = text
    # 将长度扩充到20以上，增加guessLanguage检测精确性
    while len(_text) < 20:
        _text += _text
    language = guessLanguage(_text)
    if language in ('en', 'zh'):
        return language
    # Unicode只有一个字符集，中、日、韩的三种文字占用了Unicode中0x3000到0x9FFF的部分
    for ch in text:
        if ord(ch) > 0x3000:
            return 'zh'
    return 'en'
