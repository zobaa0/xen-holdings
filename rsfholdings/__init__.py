import celery
from .celery import app as celery_app

_all__ = ('celery_app',)