from collections.abc import Sequence
from typing import List

from sqlmodel import select, update, delete
from app.models import Lesson, Session, engine, Module, User
from app.models.user_accesses_lesson import UserAccessesLessonLink
from app.schemas.lesson import LessonForm, LessonResponse, LessonNestedForm


class LessonService:
    @classmethod
    def get_instances_from_data(cls, lessons_forms: List[LessonNestedForm]) -> List[Lesson]:
        return [
            Lesson(
                title=lesson_form.title,
                position=i,
                video_link=lesson_form.video_link,
            )
            for i, lesson_form in enumerate(lessons_forms)
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

    @classmethod
    def register(cls, lesson_form: LessonForm, module: Module) -> Lesson:
        with Session(engine) as session:
            lesson = Lesson(
                title=lesson_form.title,
                position=lesson_form.position,
                video_link=lesson_form.video_link,
                module=module
            )

            session.add(lesson)
            session.commit()
            session.refresh(lesson)

            return lesson

    @classmethod
    def get_by_id(cls, lesson_id: int):
        with Session(engine) as session:
            return session.get(Lesson, lesson_id)

    @classmethod
    def update(cls, edited_data: LessonForm, lesson: Lesson):
        with Session(engine) as session:
            session.exec(
                update(Lesson)
                .where(Lesson.id == lesson.id)
                .values(
                    title=edited_data.title,
                    position=edited_data.position,
                    video_link=edited_data.video_link,
                )
            )

            session.commit()

    @classmethod
    def delete(cls, lesson: Lesson):
        with Session(engine) as session:
            session.delete(lesson)
            session.commit()

    @classmethod
    def register_user_access(cls, lesson: Lesson, current_user: User) -> None:
        with Session(engine) as session:
            if cls.has_user_already_accessed_lesson(lesson, current_user):
                return

            access = UserAccessesLessonLink(
                user_id=current_user.id,
                lesson_id=lesson.id
            )

            session.add(access)
            session.commit()

    @classmethod
    def has_user_already_accessed_lesson(cls, lesson: Lesson, user: User) -> bool:
        with Session(engine) as session:
            access = session.scalars(
                select(UserAccessesLessonLink)
                .where((UserAccessesLessonLink.user_id == user.id) & (UserAccessesLessonLink.lesson_id == lesson.id))
            ).first()

            return bool(access)
