from collections.abc import Sequence
from typing import List

from sqlmodel import select
from app.models import Lesson, Session, engine
from app.schemas.lesson import LessonForm, LessonResponse


class LessonService:
    @classmethod
    def get_instances_from_data(cls, lessons_forms: List[LessonForm]) -> List[Lesson]:
        return [
            Lesson(
                title=lesson_form.title,
                position=lesson_form.position,
                video_link=lesson_form.video_link,
            )
            for lesson_form in lessons_forms
        ]

    @classmethod
    def to_response(cls, lesson: Lesson) -> LessonResponse:
        return LessonResponse(
            id=lesson.id,
            title=lesson.title,
            position=lesson.position,
            video_link=lesson.video_link,
        )

    @classmethod
    def get_related_to_module(cls, module_id: int) -> Sequence[Lesson]:
        with Session(engine) as session:
            return session.scalars(
                select(Lesson).where(Lesson.module_id == module_id)
            ).all()
