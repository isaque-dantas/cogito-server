from fastapi.testclient import TestClient

from app import app
from app.models import db, Course, User
from app.schemas.course import CourseForm
from app.schemas.lesson import LessonNestedForm
from app.schemas.module import ModuleNestedForm
from app.schemas.user import UserForm

client = TestClient(app)

example_test_data = {
    'user': UserForm(name='name', password='password', email='test-email@email.com', cpf='73990286056'),

    'course': CourseForm(
        title="(test) Introdução à computação gráfica com Blender I",
        modules=[
            ModuleNestedForm(
                title="Módulo 1 - Visão geral",
                lessons=[
                    LessonNestedForm(title="Introdução ao uso do Blender", video_link="link"),
                    LessonNestedForm(title="Instalação do Blender (Windows, Ubuntu e MacOs)", video_link="link"),
                    LessonNestedForm(title="Visão geral da interface gráfica", video_link="link"),
                ]
            ),
            ModuleNestedForm(
                title="Módulo 2 - Visão geral",
                lessons=[
                    LessonNestedForm(title="Introdução ao uso do Blender", video_link="link"),
                    LessonNestedForm(title="Instalação do Blender (Windows, Ubuntu e MacOs)", video_link="link"),
                    LessonNestedForm(title="Visão geral da interface gráfica", video_link="link"),
                ]
            ),
        ]
    )
}

NUMBER_OF_LESSONS_IN_EXAMPLE_DATA = 6


def reset_database():
    with db.atomic():
        (
            Course
            .delete()
            .where(Course.title == example_test_data['course'].title)
        ).execute()

        (
            User
            .delete()
            .where(User.email == example_test_data['user'].email)
        ).execute()
