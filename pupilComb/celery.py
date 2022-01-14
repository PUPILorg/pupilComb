import os

from celery import Celery
from celery.utils.log import get_task_logger


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pupilComb.settings')

app = Celery('pupilComb')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

logger = get_task_logger(__name__)