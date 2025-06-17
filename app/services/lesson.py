from collections.abc import Sequence
from typing import List, Optional

from fastapi import Depends

from sqlmodel import select, update, delete
from app.models import Lesson, Session, engine, Module, User, SessionDep
from app.models.user_accesses_lesson import UserAccessesLessonLink
from app.schemas.lesson import LessonForm, LessonResponse, LessonNestedForm, LessonStatus


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
    def to_response(cls, lesson: Lesson, user_requesting_access: Optional[User] = None) -> LessonResponse:
        lesson_status_for_user: LessonStatus = LessonService.get_lesson_status_for_user(lesson, user_requesting_access)

        should_include_video_link = (
                user_requesting_access is not None
                and
                lesson_status_for_user != LessonStatus.LOCKED
        )

        return LessonResponse(
            id=lesson.id,
            title=lesson.title,
            position=lesson.position,
            video_link=lesson.video_link if should_include_video_link else None,
        )

    @classmethod
    def get_related_to_module(cls, module_id: int, session: Session = Depends(SessionDep)) -> Sequence[Lesson]:
        return session.scalars(
            select(Lesson).where(Lesson.module_id == module_id)
        ).all()

    @classmethod
    def register(cls, lesson_form: LessonForm, module: Module, session: Session = Depends(SessionDep)) -> Lesson:
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
    def get_by_id(cls, lesson_id: int, session: Session = Depends(SessionDep)):
        return session.get(Lesson, lesson_id)

    @classmethod
    def update(cls, edited_data: LessonForm, lesson: Lesson, session: Session = Depends(SessionDep)):
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
    def delete(cls, lesson: Lesson, session: Session = Depends(SessionDep)):
        session.delete(lesson)
        session.commit()

    @classmethod
    def register_user_access(cls, lesson: Lesson, user: User, session: Session = Depends(SessionDep)) -> None:
        if cls.has_user_already_accessed_lesson(lesson, user):
            return

        access = UserAccessesLessonLink(
            user_id=user.id,
            lesson_id=lesson.id
        )

        session.add(access)
        session.commit()

    @classmethod
    def has_user_already_accessed_lesson(cls, lesson: Lesson, user: User,
                                         session: Session = Depends(SessionDep)) -> bool:
        access = session.scalars(
            select(UserAccessesLessonLink)
            .where(
                (UserAccessesLessonLink.user_id == user.id)
                &
                (UserAccessesLessonLink.lesson_id == lesson.id)
            )
        ).first()

        return bool(access)

    @classmethod
    def get_lesson_status_for_user(cls, lesson: Lesson, user: User) -> LessonStatus:
        previous_lesson: Optional[Lesson] = cls.get_previous_lesson(lesson)
        if previous_lesson is None:
            return LessonStatus.ACCESSIBLE

        if not cls.has_user_already_accessed_lesson(previous_lesson, user):
            return LessonStatus.LOCKED

        if cls.has_user_already_accessed_lesson(lesson, user):
            return LessonStatus.ACCESSED

        return LessonStatus.ACCESSIBLE

    @classmethod
    def get_previous_lesson(cls, lesson: Lesson, session: Session = Depends(SessionDep)) -> Optional[Lesson]:
        if lesson.position == 0 and lesson.module.position == 0:
            return None

        return session.scalar(
            select(Lesson)
            .where(
                (Lesson.position == (lesson.position - 1))
                &
                (Lesson.module.course == lesson.module.course)
            )
        )
