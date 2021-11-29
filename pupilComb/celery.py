import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pupilComb.settings')

app = Celery('pupilComb')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()