from fastapi import FastAPI
from src.app.api.v1 import task_routers, auth
from src.app.core.config import settings

app = FastAPI()

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(task_routers.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to Audio Prompt API"}