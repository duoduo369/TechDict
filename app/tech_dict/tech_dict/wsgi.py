#!/usr/bin/env python
# coding: utf-8
"""
WSGI config for tech_dict project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/howto/deployment/wsgi/
"""
import sys

# 将系统的编码设置为UTF8
reload(sys)
sys.setdefaultencoding('utf8')
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tech_dict.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
