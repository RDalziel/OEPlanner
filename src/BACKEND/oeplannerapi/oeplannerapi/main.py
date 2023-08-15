from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import traceback
from fastapi import Query
from oeplannertasks import celery_app
from pydantic import UUID4, BaseModel
from oeplannertasks import tasks

app = FastAPI()
celery = celery_app.app


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    stack_trace = traceback.format_exc()
    return JSONResponse(
        status_code=500,
        content={"message": str(exc), "stack_trace": stack_trace}
    )


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
    task_info = celery_app.app.AsyncResult(str(task_id))
    task_result = task_info.result
    if isinstance(task_result, Exception):
        task_result = None
    return TaskStatusResponse(task_id=task_id, status=task_info.status, result=task_result)


@app.get("/wait", response_model=CeleryTaskResponse)
def wait(
        seconds: int = Query(10, description="number of seconds to wait"),
        fail: bool = Query(False, description="cause the task to fail"),
) -> CeleryTaskResponse:
    task = tasks.wait_for.delay(seconds=seconds, fail=fail)
    return CeleryTaskResponse(task_id=task.id)
