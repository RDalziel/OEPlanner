from celery import Celery


def configure(app: Celery):
    print(f'Running with RMQ Broker')
