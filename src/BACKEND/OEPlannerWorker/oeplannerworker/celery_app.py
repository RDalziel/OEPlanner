import os
from time import sleep

from celery import Celery

app = Celery('oeplannerworker', broker=os.getenv('CELERY_BROKER_URL'))
@app.task(name="wait_for")
def wait_for(seconds: int, fail: bool = False) -> str:
    if fail:
        raise RuntimeError
    sleep(seconds)
    return f"Waited for {seconds} seconds."
