from fastapi import FastAPI
from .routers import auth, subject, challenge, progress

app = FastAPI(title="Math Battle API")

app.include_router(auth.router)
app.include_router(subject.router)
app.include_router(challenge.router)
app.include_router(progress.router)
