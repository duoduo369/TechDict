from __future__ import absolute_import
from rest_framework.views import APIView
from .filters import Filters

class BaseView(APIView):
    '''
        base view
    '''
