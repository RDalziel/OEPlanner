from fastapi import FastAPI
from fastapi import Query
from oeplannerworker import celery_app
from pydantic import UUID4, BaseModel

from . import celery_app

app = FastAPI()

class CeleryTaskResponse(BaseModel):
    task_id: UUID4

class TaskStatusResponse(BaseModel):
    task_id: UUID4
    status: str
    result: str | None

class CeleryTaskIdList(BaseModel):
    task_ids: list[str]

class CeleryTaskStatistics(BaseModel):
    total: int
    pending: int
    succeeded: int
    failed: int

    @property
    def success_rate(self) -> float:
        return (self.succeeded / self.total) if self.total > 0 else 1

@app.get("/status/{task_id}", response_model=TaskStatusResponse)
def status(task_id: UUID4) -> TaskStatusResponse:
    task_info = celery_app.celery.AsyncResult(str(task_id))
    task_result = task_info.result
    if isinstance(task_result, Exception):
        task_result = None
    return TaskStatusResponse(task_id=task_id, status=task_info.status, result=task_result)


@app.get("/wait", response_model=CeleryTaskResponse)
def wait(
        seconds: int = Query(10, description="number of seconds to wait"),
        fail: bool = Query(False, description="cause the task to fail"),
) -> CeleryTaskResponse:
    task = celery_app.wait_for.delay(seconds=seconds, fail=fail)
    return CeleryTaskResponse(task_id=task.id)
