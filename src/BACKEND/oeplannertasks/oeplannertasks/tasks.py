from time import sleep
from .celery_app import app


@app.task(name="wait_for")
def wait_for(seconds: int, fail: bool = False) -> str:
    if fail:
        raise RuntimeError
    sleep(seconds)
    return f"Waited for {seconds} seconds."
