from celery import Celery
from kombu import Queue
import os

def configure(app: Celery):
    print(f'Running with ASB Broker')
    app.conf.broker_pool_limit = 10
    app.conf.broker_connection_max_retries = 0
    app.conf.broker_transport = 'azureservicebus.transport.ServiceBusTransport'

    app.conf.task_queues = (
        Queue('celery', routing_key='celery'),
    )

    app.conf.task_default_queue = 'celery'
    app.conf.task_default_exchange = 'celery'
    app.conf.task_default_routing_key = 'celery'
