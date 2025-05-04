from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.controllers import auth_router, project_router, user_router

app = FastAPI(title="Fast API", version="1.0")

origins = [
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/api/v1")
app.include_router(user_router, prefix="/api/v1")
app.include_router(project_router, prefix="/api/v1")
