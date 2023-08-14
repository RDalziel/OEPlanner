import os

from kombu import Queue
from time import sleep

from celery import Celery

celery = Celery(__name__)
celery.conf.broker_url = os.environ['OEPlanner_ASB_ENDPOINT']
celery.conf.broker_pool_limit = 10
celery.conf.broker_connection_max_retries = 0
celery.conf.broker_transport_options = {
    'pre_settled': True,
    'creds': ('RootManageSharedAccessKey', os.environ['OEPlanner_ASB_SharedAccessKey'])}
celery.conf.broker_transport = 'azureservicebus.transport.ServiceBusTransport'

celery.conf.task_queues = (
    Queue('celery', routing_key='celery'),
)

celery.conf.task_default_queue = 'celery'
celery.conf.task_default_exchange = 'celery'
celery.conf.task_default_routing_key = 'celery'


@celery.task(name="wait_for")
def wait_for(seconds: int, fail: bool = False) -> str:
    if fail:
        raise RuntimeError
    sleep(seconds)
    return f"Waited for {seconds} seconds."


if __name__ == '__main__':
    celery.worker_main()
