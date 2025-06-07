from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.models import create_db_and_tables, SessionDep
from app import models
from app.routers.user import router as user_router
from app.routers.auth import router as auth_router
from app.routers.course import router as course_router
from app.routers.module import router as module_router
from app.routers.lesson import router as lesson_router

@asynccontextmanager
async def lifespan(_: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(user_router)
app.include_router(auth_router)
app.include_router(course_router)
app.include_router(module_router)
app.include_router(lesson_router)
