from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.models import create_db_and_tables
from app import models

@asynccontextmanager
async def lifespan(fast_app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)
