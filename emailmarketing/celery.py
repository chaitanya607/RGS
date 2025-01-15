from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
import kombu

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'emailmarketing.settings')

app = Celery('emailmarketing')

# Load task modules from all registered Django app configs.
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

# Avoid custom logging configuration
app.conf.worker_hijack_root_logger = False
