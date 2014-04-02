#!coding: utf-8
'''
    执行此脚本时 必须在项目目录下 而不是scripts 下 
    此脚本在有数据库表结构更改时使用 使用工具: South
    使用方法:

      git pull 之前
        python scripts/south_migrate.py init app1,app2,app3

      git pull 之后
        python scripts/south_migrate.py auto app1,app2,app3
'''

import os
import sys
import subprocess

from os.path import realpath, dirname
from os.path import join as path_join
sys.path.insert(
    0,
    realpath(path_join(dirname(__file__), '../'))
)


os.environ['DJANGO_SETTINGS_MODULE'] = 'tech_dict.settings'

from django.db import connection
from django.conf import settings


def get_args(argvs):
    '''
        获取输入参数
        返回:
            操作action => init auto
            有变更的app => [app1, app2, app3]
    '''

    try:
        action = argvs[1]
        apps = [i.strip() for i in argvs[2].split(',') if i.strip()]
    except Exception:
        print 'ERROR: action and apps is needed!'
        exit()

    if action not in ('init', 'auto'):
        print 'ERROR: action must in (init, auto)'
        exit()

    not_in = False
    installed_apps = settings.INSTALLED_APPS
    for app in apps:
        if app not in installed_apps:
            not_in = True
            print 'ERROR: App %s is not exist !' % app

    if not_in:
        exit()

    return action, apps


def delete_south_migrationhistory():
    '''清空 south 之前的数据'''

    cursor = connection.cursor()
    count = cursor.execute('select * from south_migrationhistory')
    if count:
        print 'south_migrationhistory: ', count
        cursor.execute('delete from south_migrationhistory')

def delete_migrations_dir(apps):
    '''删除生成的 migrations 临时目录'''

    for app in apps:
        migrations = '%s/migrations' % app
        if os.path.exists(migrations):
            commond = 'mv %s/ /tmp/' % migrations
            print commond
            subprocess.check_output(commond.split(' '))


def init_migrate(apps):
    '''
        South 初始化 操作
    '''

    print 'Init START ...\n'

    delete_south_migrationhistory()
    for app in apps:
        commond = 'python manage.py schemamigration %s --initial' % app
        print commond
        print subprocess.check_output(commond.split(' ')), '\n'

        commond = 'python manage.py migrate %s 0001 --fake' % app
        print commond
        print subprocess.check_output(commond.split(' ')), '\n'

    print 'Init OK\n'


def auto_migrate(apps):

    print 'Auto START ...\n'

    for app in apps:
        commond = 'python manage.py schemamigration %s --auto' % app
        print commond
        print subprocess.check_output(commond.split(' ')), '\n'

        commond = 'python manage.py migrate %s' % app
        print commond
        print subprocess.check_output(commond.split(' ')), '\n'

    delete_south_migrationhistory()
    delete_migrations_dir(apps)

    print 'Auto OK\n'

if __name__ == '__main__':

    action, apps = get_args(sys.argv)
    if action == 'init':
        init_migrate(apps)
    elif action == 'auto':
        auto_migrate(apps)
    else:
        print 'No action'
