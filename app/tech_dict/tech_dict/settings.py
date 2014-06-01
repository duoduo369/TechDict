# -*- coding: utf-8 -*-
"""
Django settings for tech_dict project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import sys
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
LOG_DIR = os.path.join(BASE_DIR, 'log')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'x@18g06lly@wn@vla#bh&ms)^-jbtmo3lk8z2g55o7r#@t&lyb'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False
#DEBUG = True

TEMPLATE_DEBUG = DEBUG

#ALLOWED_HOSTS = ['*',]
#ALLOWED_HOSTS = []
ALLOWED_HOSTS = [
    'localhost', # for debug
    '127.0.0.1', # for debug
    'django', # server_name www.api.tect_dict.com;
              # location / 下的
              # nginx proxy_pass http://django;
    '115.28.11.182', # 61 hosts
]
#ALLOWED_HOSTS = '*'

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'djcelery',
    'south',
    'rest_framework',
    'corsheaders',
    'sites',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

CORS_ORIGIN_ALLOW_ALL = True

ROOT_URLCONF = 'tech_dict.urls'

WSGI_APPLICATION = 'tech_dict.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases
DB_MASTER = 'default'

DATABASES = {
    DB_MASTER: {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'tech_dict',
        'USER': 'root',
        'PASSWORD': '',
        'HOST': '127.0.0.1',
        'PORT': '',                      # Set to empty string for default.
    },
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/
STATIC_ROOT = './'
STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
    os.path.join(BASE_DIR, "admin"),
    os.path.join(BASE_DIR, "rest_framework"),
)
print STATICFILES_DIRS
#------------------------- rest ---------------------

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication'
    ),
    'EXCEPTION_HANDLER': 'tech_dict.custom_exceptions.custom_exception_handler',
}

#------------------------- logging ---------------------

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'standard': {
            'format': '[%(asctime)s] Level:%(levelname)s location:%(pathname)s\
                       FuncName:%(funcName)s Line:%(lineno)d Message:%(message)s',
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'sites': {
            'level':'DEBUG',
            'class':'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOG_DIR, 'sites.log'),
            'maxBytes': 1024*1024*50, # 50 MB
            'backupCount': 10,
            'formatter':'standard',
        },
    },
    'loggers': {
        'sites': {'handlers': ['sites'], 'level': 'DEBUG', 'propagate': True},
    }
}

# ----------------------------  celery ------------
import djcelery
djcelery.setup_loader()

# broker 用的rabbitmq
#BROKER_URL = 'amqp://social_master:admaster@127.0.0.1:5672/social_crm'
BROKER_URL = 'amqp://duoduo:duoduo@127.0.0.1:5672/duoduo_host'

# 这是使用了django-celery默认的数据库调度模型,任务执行周期都被存在你指定的orm数据库中
CELERYBEAT_SCHEDULER = 'djcelery.schedulers.DatabaseScheduler'

CELERYD_CONCURRENCY = 2  # celery worker的并发数 也是命令行-c指定的数目
CELERYD_PREFETCH_MULTIPLIER = 1  # celery worker 每次去rabbitmq取任务的数量
CELERYD_MAX_TASKS_PER_CHILD = 100 # 每个worker执行了多少任务就会死掉

CELERY_RESULT_BACKEND = "amqp" # 官网优化的地方也推荐使用c的librabbitmq
CELERY_RESULT_SERIALIZER = 'json' # 默认是pickle
CELERY_TASK_SERIALIZER = 'json'
CELERY_DEFAULT_QUEUE = 'default' # 默认队列名称
CELERY_DEFAULT_EXCHANGE = 'default'  # 默认交换
CELERY_DEFAULT_EXCHANGE_TYPE = 'direct'  # 默认交换类型
CELERY_DEFAULT_ROUTING_KEY = 'default'  # 默认路由key

CELERY_IGNORE_RESULT = True
CELERY_STORE_ERRORS_EVEN_IF_IGNORED = False
CELERY_AMQP_TASK_RESULT_EXPIRES = 18000

CELERY_EXPIRES_TIME = 18000 # 过期时间 单位s

CONN_MAX_AGE = 10

CELERY_IMPORTS = ('sites',)

# 队列配置
keys = list(CELERY_IMPORTS)
keys.extend(['default', 'backend_cleanup'])
CELERY_QUEUES = {}
for key in keys:
    CELERY_QUEUES[key] = {
        'exchange': key,
        'exchange_type': 'direct',
        'routing_key': key,
    }

class MyRouter(object):

    def route_for_task(self, task, args=None, kwargs=None):

        _mapper = {
            'sites.tasks': {'queue': 'sites'},
            'celery.backend_cleanup': {'queue': 'backend_cleanup'},
        }

        queue = None
        for key in _mapper:
            if task.startswith(key):
                queue = _mapper[key]
                break

        if not queue:
            print 'DEFAULT_TASK_%s' % task

        return queue

CELERY_ROUTES = (MyRouter(), )
