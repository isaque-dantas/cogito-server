from datetime import datetime
from typing import Optional

from sqlalchemy.sql.expression import text
from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlmodel import Field, SQLModel


class UserSubscribesInCourseLink(SQLModel, table=True):
    user_id: int = Field(default=None, primary_key=True, foreign_key="user.id")
    course_id: int = Field(default=None, primary_key=True, foreign_key="course.id")
    timestamp: Optional[datetime] = Field(
        default=None,
        sa_column=Column(
            TIMESTAMP(timezone=True),
            nullable=False,
            server_default=text("CURRENT_TIMESTAMP")
        )
    )
