import multiprocessing
BASE_PATH = '/opt/TechDict'
#bind = "0:8000"
bind = "127.0.0.1:8000"
workers = multiprocessing.cpu_count()

max_requests = 5000

user = 'duoduo'
group = 'duoduo'

accesslog = BASE_PATH + '/gunicorn/log/gunicorn_access.log'
errorlog = BASE_PATH + '/gunicorn/log/gunicorn_error.log'
chdir = BASE_PATH + '/app/tech_dict'
print 'accesslog:', accesslog
print 'errorlog:', errorlog
print 'chdir:', chdir
