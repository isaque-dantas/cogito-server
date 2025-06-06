import os.path

from sqlmodel import Session, create_engine, SQLModel
from typing import Annotated
from fastapi import Depends
from alembic.config import Config as AlembicConfig

from app.models.user import User
from app.models.course import Course
from app.models.module import Module
from app.models.lesson import Lesson

alembic_config_path = os.path.join(os.path.dirname(__file__), '../../alembic.ini')
url = AlembicConfig(alembic_config_path).get_main_option("sqlalchemy.url")
engine = create_engine(url)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]
