from oeplannertasks import celery_app
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import traceback

app = FastAPI()
celery = celery_app.app

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    stack_trace = traceback.format_exc()
    return JSONResponse(
        status_code=500,
        content={"message": str(exc), "stack_trace": stack_trace}
    )


@app.on_event("startup")
async def startup():
    celery.Worker(app=celery).start()


@app.get("/health")
async def health():
    result = celery.control.ping()
    if not result:
        raise Exception("Celery ping failed!")
    return {"status": "ok"}
