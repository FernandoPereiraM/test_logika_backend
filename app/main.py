from fastapi import FastAPI
from app.api import auth, tasks

app = FastAPI(title="Technical Test API")

app.include_router(auth.router)
app.include_router(tasks.router)
