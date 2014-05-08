#coding: utf-8
'''
    自定义异常错误 及异常handler
'''

import json

from rest_framework import exceptions
from rest_framework.views import exception_handler

MISSING = 'missing'
MISSING_FIELD = 'missing_field'
INVALID = 'invalid'
EXISTS = 'already_exists'


class ArgumentError(exceptions.APIException):
    '''参数错误'''

    status_code = 422
    default_detail = ''

    def __init__(self, detail=None, errors=None):

        if errors:
            detail = 'errors||%s' % json.dumps(errors)
        self.detail = detail or self.default_detail


def custom_exception_handler(exc):
    '''
        自定义异常handler
        django rest 的异常返回为{'detail': 'Error message'}
        我们需求的异常返回为{
            'message': 'Error message',
            'errors': {
                'email': 'missing',
            },
        }
        missing: 这意味着资源不存在
        missing_field: 这意味着对资源所需的领域尚未确定
        invalid: 这意味着领域格式不合法。资源文档应该给您提供更专业的信息。
        already_exists: 这意味着已经存在和该领域同样值的资源了。这就要求要有独立的key
    '''

    # 获取django标准的异常response
    response = exception_handler(exc)
    if response is not None:
        message = response.data.get('detail', '')
        errors = {}
        if message.startswith('errors||'):
            errors = json.loads(message.split('||')[1])
            message = 'Validation Failed'
        response.data = {'message': message, 'errors': errors}
        return response
