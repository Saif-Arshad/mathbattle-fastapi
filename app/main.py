from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers import auth, subject, challenge, progress,admin,parent,teacher

app = FastAPI(title="Math Battle API")

origins = [
    "http://localhost",           
    "http://localhost:3000",      
    "http://127.0.0.1:5500",     
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,        
    allow_credentials=True,
    allow_methods=["*"],         
    allow_headers=["*"],           
)

# 2. Include your routers
app.include_router(auth.router)
app.include_router(subject.router)
app.include_router(challenge.router)
app.include_router(progress.router)
app.include_router(admin.router) 
app.include_router(parent.router) 
app.include_router(teacher.router) 

