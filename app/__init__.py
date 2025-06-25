from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.middlewares.i18n import I18nMiddleware
from app.models import create_db_and_tables
from app import models
from app.routers.user import router as user_router
from app.routers.auth import router as auth_router
from app.routers.course import router as course_router
from app.routers.module import router as module_router
from app.routers.lesson import router as lesson_router

@asynccontextmanager
async def lifespan(_):
    create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["http://localhost:4200", "http://127.0.0.1:4200"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(I18nMiddleware)

app.include_router(user_router)
app.include_router(auth_router)
app.include_router(course_router)
app.include_router(module_router)
app.include_router(lesson_router)
