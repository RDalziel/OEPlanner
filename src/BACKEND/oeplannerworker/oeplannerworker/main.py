from oeplannertasks import celery_app
from fastapi import FastAPI

app = FastAPI()
celery = celery_app.app


@app.on_event("startup")
async def startup():
    celery.start()

@app.get("/health")
async def health():
  result = app.celery.control.ping()
  if not result:
    raise Exception("Celery ping failed!")
  return {"status": "ok"}
