from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.models import create_db_and_tables, SessionDep
from app import models
from app.routers.user import router as user_router

@asynccontextmanager
async def lifespan(fast_app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(user_router)
