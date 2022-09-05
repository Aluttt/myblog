import os

from celery import Celery

os.environ['DJANGO_SETTINGS_MODULE'] = 'myblog.settings'
os.environ.setdefault('DJANGO_SENTTINGS_MODULE','myblog.settings')


broker = 'redis://127.0.0.1:6379/0'  # 无密码
# 任务结果存储
backend = 'redis://127.0.0.1:6379/1'

app = Celery('myblog', broker=broker, backend=backend)

app.autodiscover_tasks(['user.tasks'])