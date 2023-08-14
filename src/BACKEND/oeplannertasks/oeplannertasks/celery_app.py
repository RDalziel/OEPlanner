import os

from celery import Celery

from .app_asb_conf import configure as asb_configure
from .app_rmq_conf import configure as rmq_configure

app = Celery(__name__,
             broker=os.getenv('CELERY_BROKER_URL'),
             include='oeplannertasks.tasks')

transport = os.getenv('CELERY_TRANSPORT')

if transport == 'ASB':
    asb_configure(app)

elif transport == 'RMQ':
    rmq_configure(app)
