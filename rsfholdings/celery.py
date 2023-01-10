import os
from celery import Celery

# Set the default Django settings module for  the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rsfholdings.settings')

# Create an instance of the app
app = Celery('rsfholdings')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration
# keys should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Auto discovers asynchronous tasks in each app
app.autodiscover_tasks()