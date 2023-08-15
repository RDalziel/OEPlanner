import os

from celery import Celery

app = Celery(__name__,
             broker=os.getenv('CELERY_BROKER_URL'),
             include='oeplannertasks.tasks')